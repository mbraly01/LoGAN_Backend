import boto3

#create instance of resource class


class Gallery:

    def __init__(self):
        self.gallery = []
        self.s3 = boto3.resource("s3")
        self.s3_client = boto3.client("s3")
        self.bucket = self.s3.Bucket("thegallery")

    def add_to_gallery(self, brand_name, number):
        self.s3_client.upload_file(f"/home/mbraly/python-for-byte-academy/Final_Project/Website/matapp/my-app/src/output/img{number}.jpg","thegallery",f"{brand_name}.jpg")

    def make_gallery(self):
        items = []
        for item in self.bucket.objects.all():
            stripped_item = item.key.strip(".jpg")
            items.append(stripped_item)
            self.s3.meta.client.download_file("thegallery",item.key,f"/home/mbraly/python-for-byte-academy/Final_Project/Website/matapp/my-app/public/gallery/{item.key}")
        return items

