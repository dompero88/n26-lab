#!/usr/bin/env python3
import os
import aws_cdk as cdk

# IMPORTANTE: Nota il doppio "infra" perché la tua cartella si chiama così
from infra.infra_stack import InfraStack 

app = cdk.App()

InfraStack(app, "InfraStack",
    env = cdk.Environment(account="146040387806", region="eu-central-1") 
)
app.synth()
