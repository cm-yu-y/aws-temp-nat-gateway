#!/usr/bin/env python3
import aws_cdk as cdk
from aws_temp_nat_gateway.aws_temp_nat_gateway_stack import NatGatewayStack

# CDKアプリケーションの初期化
app = cdk.App()

# CDKコマンド引数から環境を取得（デフォルトは'dev'）
env_name = app.node.try_get_context("env") or "dev"

# 環境固有の設定を取得
environments = app.node.try_get_context("environments") or {}
env_config = environments.get(env_name, {})

# AWS環境設定
aws_account = env_config.get("account")
aws_region = env_config.get("region")

if not env_config:
    raise ValueError(f"Environment '{env_name}' configuration not found in context")

vpc_id = env_config.get("vpc_id", "")
public_subnet_id = env_config.get("public_subnet_id", "")
route_table_ids = env_config.get("route_table_ids", [])

# 環境固有のスタック名を作成
stack_name = f"NatGatewayStack-{env_name}"

# スタックに引数を渡す
NatGatewayStack(
    app,
    stack_name,
    vpc_id=vpc_id,
    public_subnet_id=public_subnet_id,
    route_table_ids=route_table_ids,
    # 環境情報を指定
    env=cdk.Environment(
        account=aws_account,
        region=aws_region
    )
)

# テンプレートの合成
app.synth()