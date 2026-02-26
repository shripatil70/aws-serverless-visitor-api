import boto3
import zipfile
import time
import json
import os

region = "ap-south-1"
lambda_function_name = "VisitorGreetingFunction"
api_name = "VisitorGreetingAPI"
table_name = "VisitorLogs"

# 🔴 Replace with your IAM Role ARN
role_arn = "arn:aws:iam::475411230755:role/LambdaExecutionRole"

lambda_client = boto3.client("lambda", region_name=region)
apigateway = boto3.client("apigatewayv2", region_name=region)
dynamodb = boto3.client("dynamodb", region_name=region)

# -------------------------------------------------
# 1️⃣ Create DynamoDB Table
# -------------------------------------------------

try:
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "visitor_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "visitor_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
    print("Creating DynamoDB table...")
    time.sleep(10)
except dynamodb.exceptions.ResourceInUseException:
    print("DynamoDB table already exists.")

# -------------------------------------------------
# 2️⃣ Zip Lambda Code (app.py)
# -------------------------------------------------

with zipfile.ZipFile("lambda_function.zip", "w") as zipf:
    zipf.write("app.py")

# -------------------------------------------------
# 3️⃣ Create Lambda Function
# -------------------------------------------------

try:
    response = lambda_client.create_function(
        FunctionName=lambda_function_name,
        Runtime="python3.12",
        Role=role_arn,
        Handler="app.lambda_handler",
        Code={"ZipFile": open("lambda_function.zip", "rb").read()},
        Timeout=10,
        Publish=True
    )
    lambda_arn = response["FunctionArn"]
    print("Lambda Created:", lambda_arn)
except lambda_client.exceptions.ResourceConflictException:
    lambda_arn = lambda_client.get_function(
        FunctionName=lambda_function_name
    )["Configuration"]["FunctionArn"]
    print("Lambda already exists.")

time.sleep(5)

lambda_client.update_function_code(
    FunctionName=lambda_function_name,
    ZipFile=open("lambda_function.zip", "rb").read()
)
print("Lambda code updated.")

# -------------------------------------------------
# 4️⃣ Create API Gateway
# -------------------------------------------------

api_response = apigateway.create_api(
    Name=api_name,
    ProtocolType="HTTP"
)

api_id = api_response["ApiId"]
print("API Created:", api_id)

# -------------------------------------------------
# 5️⃣ Create Integration
# -------------------------------------------------

integration = apigateway.create_integration(
    ApiId=api_id,
    IntegrationType="AWS_PROXY",
    IntegrationUri=lambda_arn,
    PayloadFormatVersion="2.0"
)

integration_id = integration["IntegrationId"]

# -------------------------------------------------
# 6️⃣ Create Routes (GET + POST)
# -------------------------------------------------

apigateway.create_route(
    ApiId=api_id,
    RouteKey="GET /greet",
    Target=f"integrations/{integration_id}"
)

apigateway.create_route(
    ApiId=api_id,
    RouteKey="POST /greet",
    Target=f"integrations/{integration_id}"
)

# -------------------------------------------------
# 7️⃣ Create Stage
# -------------------------------------------------

apigateway.create_stage(
    ApiId=api_id,
    StageName="$default",
    AutoDeploy=True
)

# -------------------------------------------------
# 8️⃣ Add Lambda Permission
# -------------------------------------------------

import botocore

source_arn = f"arn:aws:execute-api:{region}:475411230755:{api_id}/*/*"

try:
    lambda_client.add_permission(
        FunctionName=lambda_function_name,
        StatementId="AllowAPIGatewayInvoke",
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
        SourceArn=source_arn
    )
    print("Permission added.")
except botocore.exceptions.ClientError as e:
    if e.response["Error"]["Code"] == "ResourceConflictException":
        print("Permission already exists. Skipping.")
    else:
        raise
# -------------------------------------------------
# 9️⃣ Print Final URL
# -------------------------------------------------

invoke_url = f"https://{api_id}.execute-api.{region}.amazonaws.com"
print("\n✅ Deployment Successful!")
print("Test GET:")
print("\nExample Usage:")
print(invoke_url + "/greet?name=YourName")
print("Replace 'YourName' with any visitor name.")
print("\nTest POST using Postman:")
print(invoke_url + "/greet")