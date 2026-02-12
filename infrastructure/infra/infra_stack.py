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

        # Usa la VPC di default (per semplicità e costi)
        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        # Definisci il Cluster ECS
        cluster = ecs.Cluster(self, "N26Cluster", vpc=vpc)

        # Definisci il Servizio Fargate (Load Balancer + Container)
        self.service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "N26AiService",
            cluster=cluster,
            cpu=256,            # 0.25 vCPU (Minimo costo)
            memory_limit_mib=512, # 0.5 GB RAM
            desired_count=1,
            # AGGIUNTO: Forza l'architettura x86_64 per matchare GitHub Actions
            runtime_platform=ecs.RuntimePlatform(
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                cpu_architecture=ecs.CpuArchitecture.X86_64
            ),
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("../app"),
                container_port=80,
                environment={
                    # QUI VA L'IP PRIVATO DELL'ISTANZA OLLAMA
                    "OLLAMA_ENDPOINT": "http://172.31.23.1:11434" 
                }
            ),
            public_load_balancer=True,
            assign_public_ip=True
        )