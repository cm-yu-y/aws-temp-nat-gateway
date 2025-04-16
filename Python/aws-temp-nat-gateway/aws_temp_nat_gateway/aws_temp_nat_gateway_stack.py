#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2,
    Stack,
    CfnTag,
)
from constructs import Construct

class NatGatewayStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc_id: str, public_subnet_id, route_table_ids, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        if not vpc_id:
            raise ValueError("VPC ID must be provided")
        
        if not public_subnet_id:
            raise ValueError("Public subnet ID must be provided")
        
        if not route_table_ids:
            raise ValueError("At least one route table ID must be provided")
        
        # VPCを取得
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id)
        
        # パブリックサブネットを取得
        public_subnet = ec2.Subnet.from_subnet_id(self, "PublicSubnet", public_subnet_id)
        
        # EIPの作成
        eip = ec2.CfnEIP(self, "EIP", domain="vpc")
        
        # NATゲートウェイの作成
        nat_gateway = ec2.CfnNatGateway(
            self,
            "NatGateway",
            allocation_id=eip.attr_allocation_id,
            subnet_id=public_subnet_id,
            tags=[CfnTag(key="Name", value=f"{construct_id}-NatGateway")]
        )
        
        # 複数のルートテーブルにNATゲートウェイを関連付け
        for idx, route_table_id in enumerate(route_table_ids, start=1):
            # ルートテーブルにデフォルトルートを追加
            route = ec2.CfnRoute(
                self,
                f"NatRoute{idx}",
                route_table_id=route_table_id,
                destination_cidr_block="0.0.0.0/0",
                nat_gateway_id=nat_gateway.ref
            )
            
            # ルートがNATゲートウェイに依存するように設定
            route.add_dependency(nat_gateway)