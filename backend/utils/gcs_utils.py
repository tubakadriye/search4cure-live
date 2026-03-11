from google.cloud import storage
import os
import uuid
import json

# Set GCS project and bucket
GCS_PROJECT = os.getenv("GCS_PROJECT")
GCS_BUCKET = os.getenv("GCS_BUCKET")
#path_to_credentials = "../keys/search4cure-diabetes-3919d2234efa.json"
import os

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_to_credentials


# Initialize your GCS client and bucket
gcs_client = storage.Client(project=GCS_PROJECT)
gcs_bucket = gcs_client.bucket(GCS_BUCKET)

bucket_name = "diabetes-rag-assets"

def upload_bytes_to_gcs(data, prefix) -> None:
    """
    Upload image to GCS.

    Args:
        key (str): Unique identifier for the image in the bucket.
        data (bytes): Image bytes to upload.
    """
    blob_name = f"{prefix}/{uuid.uuid4()}.png"
    blob = gcs_bucket.blob(blob_name)
    blob.upload_from_string(data, content_type="image/png")
    return blob_name


def upload_table_to_gcs(df):

    json_data = json.dumps(df.to_dict())

    gcs_key = upload_bytes_to_gcs(
        json_data.encode(),
        "tables"
    )

    return gcs_key


from io import BytesIO
from google.cloud import storage

def get_image_from_gcs(gcs_bucket, key: str) -> bytes:
    """
    Download image bytes from GCS.

    Args:
        gcs_bucket: GCS bucket instance.
        key (str): Blob key in the bucket.

    Returns:
        bytes: Image bytes.
    """
    blob = gcs_bucket.blob(key)
    return blob.download_as_bytes()