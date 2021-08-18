#create instance of resource class
s3=boto3.resource("s3")
s3_client = boto3.client("s3")
#get all buckets