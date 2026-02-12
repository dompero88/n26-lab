from aws_cdk import (
    Stack,
    Duration,                
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets,
)
from constructs import Construct

class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)
        cluster = ecs.Cluster(self, "N26Cluster", vpc=vpc)

        self.service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "N26AiService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            runtime_platform=ecs.RuntimePlatform(
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                cpu_architecture=ecs.CpuArchitecture.X86_64
            ),
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset(
                    "../app",
                    platform=ecr_assets.Platform.LINUX_AMD64 
                ),
                container_port=8080,
                environment={
                    "OLLAMA_ENDPOINT": "http://172.31.23.1:11434" 
                }
            ),
            public_load_balancer=True,
            assign_public_ip=True
        )

        # CORREZIONE: Usiamo Duration.seconds() invece di numeri interi
        self.service.target_group.configure_health_check(
            path="/health",
            interval=Duration.seconds(30),
            timeout=Duration.seconds(5),
            healthy_threshold_count=2,
            unhealthy_threshold_count=5
        )