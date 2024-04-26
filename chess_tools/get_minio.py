from minio import Minio
from minio.error import S3Error

def download_all_files(bucket_name, minio_url, access_key, secret_key, local_download_path):
    # Create a MinIO client
    client = Minio(
        minio_url,
        access_key=access_key,
        secret_key=secret_key,
        secure=False  # Set to True if using https
    )

    try:
        # List all object names in the bucket
        objects = client.list_objects(bucket_name, recursive=True)

        for obj in objects:
            # Define the local file path
            local_file_path = f"{local_download_path}/{obj.object_name}"

            ### Download the file
            client.fget_object(bucket_name, obj.object_name, local_file_path)
            print(f"Downloaded {obj.object_name} to {local_file_path}")

    except S3Error as exc:
        print("Error:", exc)

### Example usage
import os

bucket_name = 'temp'
minio_url = 'minio.pawnparse.com:9000'  # Replace with your MinIO server URL
access_key = os.getenv('MINIO_USER')  # Replace with your actual access key
secret_key = os.getenv('MINIO_PASSWORD')  # Replace with your actual secret key
local_download_path = 'temporary'  # Replace with your local download path
# if local download path not exist create it
if not os.path.exists(local_download_path):
    os.makedirs(local_download_path)

download_all_files(bucket_name, minio_url, access_key, secret_key, local_download_path)