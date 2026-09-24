import asyncio
from google.cloud import storage
import uuid

async def main():
    bucket_name = "qwiklabs-gcp-01-3c21c96f2321-static-assets-bucket"
    filename = f"instructional_video_{uuid.uuid4().hex[:8]}.mp4"
    video_bytes = b"fake_video_bytes"
    
    try:
        storage_client = storage.Client(project="qwiklabs-gcp-01-3c21c96f2321")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_string(video_bytes, content_type="video/mp4")
        
        public_url = f"https://storage.googleapis.com/{bucket_name}/{filename}"
        print(f"Success! URL: {public_url}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
