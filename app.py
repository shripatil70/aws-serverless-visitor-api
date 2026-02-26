import json
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("VisitorLogs")

def lambda_handler(event, context):

    print("EVENT:", json.dumps(event))  # Debug logging

    try:
        # 1️⃣ Extract Name (GET or POST)
        name = None

        # GET request
        if event.get("queryStringParameters"):
            name = event["queryStringParameters"].get("name")

        # POST request
        if not name and event.get("body"):
            try:
                body = json.loads(event["body"])
                name = body.get("name")
            except:
                pass

        # Validate input
        if not name or not name.strip():
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "error": "Name is required. Use ?name=YourName in URL or send JSON body with name."
                })
            }

        name = name.strip().title()

        # 2️⃣ Get IP Address (Safe for HTTP API v2)
        ip_address = (
            event.get("requestContext", {})
                 .get("http", {})
                 .get("sourceIp", "Unknown")
        )

        # 3️⃣ Current Timestamp
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # 4️⃣ Check if visitor exists
        response = table.get_item(Key={"visitor_id": name})

        if "Item" in response:
            visit_count = int(response["Item"]["visit_count"] )+ 1
        else:
            visit_count = 1

        # 5️⃣ Save / Update in DynamoDB
        table.put_item(
            Item={
                "visitor_id": name,
                "visit_count": visit_count,
                "last_visit": timestamp,
                "ip_address": ip_address
            }
        )

        # 6️⃣ Success Response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": f"Hello {name}",
                "visit_count": visit_count,
                "last_visit": timestamp,
                "ip_address": ip_address
            })
        }

    except Exception as e:
        print("ERROR:", str(e))  # Log real error to CloudWatch

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Internal Server Error",
                "details": str(e)
            })
        }