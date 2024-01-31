from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from dotenv import load_dotenv

class CloudUtils:
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv('AZURE_CONNECTION_STRING')
        self.container_name = os.getenv('AZURE_CONTAINER_NAME')

    def upload_blob(self, file_path, blob_name):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        blob_client = blob_service_client.get_blob_client(self.container_name, blob_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)