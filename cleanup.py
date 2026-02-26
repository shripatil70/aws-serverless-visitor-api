import boto3

region = "ap-south-1"
lambda_function_name = "VisitorGreetingFunction"
api_name = "VisitorGreetingAPI"
table_name = "VisitorLogs"

lambda_client = boto3.client("lambda", region_name=region)
apigateway = boto3.client("apigatewayv2", region_name=region)
dynamodb = boto3.client("dynamodb", region_name=region)

# -------------------------------------------------
# 1️⃣ Delete Lambda
# -------------------------------------------------

try:
    lambda_client.delete_function(FunctionName=lambda_function_name)
    print("Lambda deleted.")
except:
    print("Lambda not found.")

# -------------------------------------------------
# 2️⃣ Delete API Gateway
# -------------------------------------------------

apis = apigateway.get_apis()["Items"]

for api in apis:
    if api["Name"] == api_name:
        apigateway.delete_api(ApiId=api["ApiId"])
        print("API Gateway deleted.")

# -------------------------------------------------
# 3️⃣ Delete DynamoDB Table
# -------------------------------------------------

try:
    dynamodb.delete_table(TableName=table_name)
    print("DynamoDB table deleted.")
except:
    print("DynamoDB table not found.")

print("\n🧹 Cleanup Completed!")