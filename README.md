# Serverless Visitor Tracking API

## 📌 Overview
This project is a serverless REST API built using AWS Lambda, API Gateway (HTTP API), and DynamoDB.

The API tracks visitor count, stores IP address and timestamp, and returns a greeting message.

It is fully deployed on AWS using automated infrastructure provisioning with Python (Boto3).

---

## 🚀 Live API
Test the API using:

https://YOUR-API-ID.execute-api.ap-south-1.amazonaws.com/greet?name=Demo

Replace `Demo` with any name.

---

## ⚡ Performance
- Average execution time: 2 ms (measured using AWS CloudWatch)
- Auto-scaling architecture (AWS Lambda)
- Pay-per-request pricing model
- Zero idle server cost
- No EC2 required

---

## 🛠 Tech Stack
- Python 3.12
- AWS Lambda
- API Gateway (HTTP API)
- DynamoDB
- IAM (Role-based access control)
- CloudWatch (Monitoring)
- Boto3 (AWS SDK for Python)

---

## ⚙️ How It Works
1. API Gateway receives HTTP request.
2. Lambda function processes request.
3. DynamoDB stores and updates visitor count.
4. API returns greeting message with visit count, timestamp, and IP address.

---

## 🔐 Security
- IAM role-based access control (least privilege model)
- No AWS credentials stored in source code
- Uses AWS managed services

---

## 📦 Deployment

This project uses Boto3 to automate deployment.

Run:

```bash
python deploy.py
```

---

##🎯 Features

- Real-time visitor tracking
- IP address logging
- Timestamp storage
- Auto-scaling serverless architecture
- Automated infrastructure setup

---


