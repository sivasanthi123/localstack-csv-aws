import boto3
dynamodb = boto3.client("dynamodb", endpoint_url="http://localhost:4566")
table_name = "CSVMetadata"
try:
    response = dynamodb.create_table(
        TableName=table_name,
       KeySchema=[
            {
                "AttributeName": "filename",
                "KeyType": "HASH"
            }
        ],
        AttributeDefinitions=[
            {"AttributeName": "filename", "AttributeType": "S"}
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )
    print(f"Table '{table_name}' created successfully.")
except dynamodb.exceptions.ResourceInUseException:
    print(f"Table '{table_name}' already exists.")