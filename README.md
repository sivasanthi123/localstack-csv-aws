Local Cloud-Based File Processing System
This project demonstrates a local AWS environment using LocalStack to build a file processing
system.
CSV files uploaded to a local S3 bucket trigger a Lambda function to process the CSV, and
metadata is stored in DynamoDB.
---
Project Components
- S3 Bucket: To upload CSV files
- Lambda Function: Triggered by S3 events to process CSV
- DynamoDB: To store CSV metadata
- LocalStack: To emulate AWS services locally (S3, Lambda, DynamoDB)
---
Folder Structure
file-processing-project/
 docker-compose.yml
 requirements.txt
 lambda/
 process_csv.py
 infra/
 create_s3.py
 create_dynamodb.py
 deploy_lambda.py
 sample.csv
---
Prerequisites
- Docker installed and running
- Python 3.7+
- pip package manager
---
Setup Instructions
Step 1: Start LocalStack
Run the following command in your project root directory to start LocalStack services (S3, Lambda,
DynamoDB):
docker-compose up -d
This will start LocalStack on port 4566 (default edge port).
Step 2: Install Python dependencies
(Optional: Use a virtual environment)
pip install -r requirements.txt
This installs boto3 and pandas.
Step 3: Create the S3 bucket locally
Run the script to create your S3 bucket (replace bucket name if needed):
python infra/create_s3.py
You should see:
Bucket created: csv-bucket
Step 4: Create DynamoDB table locally
Run the script to create the DynamoDB table:
python infra/create_dynamodb.py
You should see either:
Table 'CSVMetadata' created successfully.
or
Table 'CSVMetadata' already exists.
Step 5: Prepare and deploy the Lambda function
Run the deployment script which packages your Lambda function, deploys it, adds the S3 trigger,
and sets permissions:
python infra/deploy_lambda.py
You should see messages like:
Created Lambda function ProcessCSVFunction
Added permission for S3 to invoke Lambda
Added S3 trigger to bucket csv-bucket
Lambda deployed and S3 trigger added.
Step 6: Upload a sample CSV file to S3 to trigger Lambda
You can upload the provided sample.csv file using AWS CLI or a Python script.
Example with AWS CLI (configured to LocalStack endpoint):
aws --endpoint-url=http://localhost:4566 s3 cp sample.csv s3://csv-bucket/
Or use a Python script snippet:
import boto3
s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
s3.upload_file('sample.csv', 'csv-bucket', 'sample.csv')
print("Uploaded sample.csv to s3://csv-bucket/sample.csv")
Step 7: Check Lambda logs and DynamoDB data
Lambda logs can be viewed in LocalStack logs or by invoking the Lambda manually.
To test Lambda function locally with sample event:
aws --endpoint-url=http://localhost:4566 lambda invoke --function-name ProcessCSVFunction
output.txt
cat output.txt
To check DynamoDB table contents:
import boto3
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
table = dynamodb.Table('CSVMetadata')
response = table.scan()
print(response['Items'])
Notes:
- Ensure your AWS CLI is configured to use LocalStack endpoint for all commands by adding
--endpoint-url=http://localhost:4566.
- Your Lambda IAM Role ARN in deploy_lambda.py is a placeholder since LocalStack does not
enforce IAM - you can leave it as is.
- Modify bucket name and region as needed in scripts.
- For production, replace LocalStack with real AWS and update roles, permissions, and endpoints.
Cleanup:
To stop LocalStack and remove containers:
docker-compose down
Summary of commands:
docker-compose up -d
pip install -r requirements.txt
python infra/create_s3.py
python infra/create_dynamodb.py
python infra/deploy_lambda.py
aws --endpoint-url=http://localhost:4566 s3 cp sample.csv s3://csv-bucket/
