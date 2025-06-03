def lambda_handler(event, context):
    print("Event:", event)
    # Your CSV processing code here
    return {"statusCode": 200, "body": "Processed CSV"}
