import csv
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
table = dynamodb.Table('CSVMetadata')

with open('sample.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # DynamoDB expects attribute values as string types for S, or numbers for N
        item = {
            'filename': row['id'],  # Use 'id' as partition key example, adjust as needed
            'name': row['name'],
            'age': int(row['age']),
            'city': row['city'],
            'date': row['date']
        }
        table.put_item(Item=item)

print("CSV data imported into DynamoDB table.")
