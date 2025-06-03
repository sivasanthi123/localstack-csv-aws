import boto3
s3= boto3.client("s3", endpoint_url="http://localhost:4566")
bucket_name="csv-bucket"
s3.create_bucket(Bucket=bucket_name)
print("Bucket created:", bucket_name)