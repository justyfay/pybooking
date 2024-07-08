import asyncio
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError

from config import settings
from src.logger import logger


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        url: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_path: str, object_name: str):
        object_name = file_path.split("/")[-1]
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name, Key=object_name, Body=file
                    )
                logger.info(f"File '{object_name}' uploaded to' {self.bucket_name}'")
        except ClientError as e:
            logger.error(f"Error uploading file: '{e}'")

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                logger.info(f"File '{object_name}' deleted from '{self.bucket_name}'")
        except ClientError as e:
            logger.error(f"Error deleting file: '{e}'")

    async def get_file_content(self, object_name: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(
                    Bucket=self.bucket_name, Key=object_name
                )
                data = await response["Body"].read()
                return data
        except ClientError as e:
            logger.error(f"Error getting file content: '{e}'")

    async def get_file(self, object_name: str, destination_path: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(
                    Bucket=self.bucket_name, Key=object_name
                )
                data = await response["Body"].read()
                with open(destination_path, "wb") as file:
                    file.write(data)
                logger.info(f"File '{object_name}' downloaded to '{destination_path}'")
        except ClientError as e:
            logger.error(f"Error downloading file: '{e}'")


async def s3_client_init():
    S3Client(
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        url=settings.s3_url,
        bucket_name="public-bucket",
    )


if __name__ == "__main__":
    asyncio.run(s3_client_init())
