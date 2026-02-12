from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
)
from constructs import Construct

class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Recupera la VPC di default
        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        # 2. Definisci il Cluster ECS
        cluster = ecs.Cluster(self, "N26Cluster", vpc=vpc)

        # 3. Definisci il Servizio Fargate (Load Balancer + Container)
        self.service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "N26AiService",
            cluster=cluster,
            cpu=256,            # 0.25 vCPU
            memory_limit_mib=512, # 0.5 GB RAM
            desired_count=1,
            # FORZA IL RUNTIME: Dice ad AWS di usare macchine Intel/AMD64
            runtime_platform=ecs.RuntimePlatform(
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                cpu_architecture=ecs.CpuArchitecture.X86_64
            ),
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                # FORZA IL BUILD: Dice a Docker di buildare in formato AMD64
                image=ecs.ContainerImage.from_asset(
                    "../app",
                    platform=ecs.AssetPlatform.LINUX_AMD64
                ),
                container_port=80,
                environment={
                    # IP PRIVATO dell'istanza EC2 dove gira Ollama
                    "OLLAMA_ENDPOINT": "http://172.31.23.1:11434" 
                }
            ),
            public_load_balancer=True,
            assign_public_ip=True
        )

        # Opzionale: Health Check personalizzato per dare tempo all'app di avviarsi
        self.service.target_group.configure_health_check(
            path="/health",
            interval=30,
            timeout=5,
            healthy_threshold_count=2,
            unhealthy_threshold_count=5
        )