import boto3
import json
import time

# AWS parameters - change these accordingly
LAMBDA_FUNCTION_NAME = 'ProcessCSVFunction'
LAMBDA_HANDLER = 'process_csv.lambda_handler'
LAMBDA_ROLE_ARN = 'your_iam_role_arn'  # replace with your IAM role arn and when creating the IAM role Must have Lambda and S3 permissions
ZIP_FILE = 'process_csv.zip'

# Set your bucket and folder (prefix) here:
S3_BUCKET = 'my-company-csv-uploads'        # <-- replace this
S3_PREFIX = ''                   # <-- replace or '' for root of bucket
S3_EVENT = 's3:ObjectCreated:*'                  

AWS_REGION = 'us-east-1'                         # <-- your AWS region here
AWS_ACCOUNT_ID = 'your_account_id'                  # Your AWS Account ID

lambda_client = boto3.client('lambda', region_name=AWS_REGION)
s3_client = boto3.client('s3', region_name=AWS_REGION)

def create_or_update_lambda():
    with open(ZIP_FILE, 'rb') as f:
        zipped_code = f.read()

    try:
        # Try to create the function
        response = lambda_client.create_function(
            FunctionName=LAMBDA_FUNCTION_NAME,
            Runtime='python3.9',  # Change if needed
            Role=LAMBDA_ROLE_ARN,
            Handler=LAMBDA_HANDLER,
            Code={'ZipFile': zipped_code},
            Timeout=30,
            MemorySize=128,
            Publish=True,
        )
        print(f"Created Lambda function {LAMBDA_FUNCTION_NAME}")
    except lambda_client.exceptions.ResourceConflictException:
        # If function exists, update code
        response = lambda_client.update_function_code(
            FunctionName=LAMBDA_FUNCTION_NAME,
            ZipFile=zipped_code,
            Publish=True,
        )
        print(f"Updated Lambda function code {LAMBDA_FUNCTION_NAME}")

    # Wait for function to be ready
    time.sleep(5)

def add_s3_trigger():
    # Get existing notification config
    bucket_notification = s3_client.get_bucket_notification_configuration(Bucket=S3_BUCKET)

    lambda_config = {
        'LambdaFunctionArn': f'arn:aws:lambda:{AWS_REGION}:{AWS_ACCOUNT_ID}:function:{LAMBDA_FUNCTION_NAME}',
        'Events': [S3_EVENT],
        'Filter': {
            'Key': {
                'FilterRules': [{'Name': 'prefix', 'Value': S3_PREFIX}]
            }
        }
    }

    existing_lambda_configs = bucket_notification.get('LambdaFunctionConfigurations', [])
    # Avoid duplicates
    if not any(conf['LambdaFunctionArn'] == lambda_config['LambdaFunctionArn'] for conf in existing_lambda_configs):
        existing_lambda_configs.append(lambda_config)

    notification_configuration = {
        'LambdaFunctionConfigurations': existing_lambda_configs
    }

    s3_client.put_bucket_notification_configuration(
        Bucket=S3_BUCKET,
        NotificationConfiguration=notification_configuration
    )
    print(f"Added S3 trigger to bucket {S3_BUCKET}")

def add_lambda_permission():
    try:
        lambda_client.add_permission(
            FunctionName=LAMBDA_FUNCTION_NAME,
            StatementId='S3InvokePermission',
            Action='lambda:InvokeFunction',
            Principal='s3.amazonaws.com',
            SourceArn=f'arn:aws:s3:::{S3_BUCKET}',
        )
        print("Added permission for S3 to invoke Lambda")
    except lambda_client.exceptions.ResourceConflictException:
        print("Permission for S3 already exists")

def main():
    create_or_update_lambda()
    add_lambda_permission()
    add_s3_trigger()
    print("Lambda deployed and S3 trigger added.")

if __name__ == '__main__':
    main()
