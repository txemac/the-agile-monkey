import base64
import binascii
from http import HTTPStatus

import boto3
from fastapi import HTTPException

import messages
import settings
from customer.domain.image_storage_service import ImageStorageService


class AWSS3ImageStorageService(ImageStorageService):
    def upload(
            self,
            path: str,
            image: str,
    ) -> None:
        boto3_session = boto3.session.Session()
        s3_client = boto3_session.resource(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            region_name=settings.S3_REGION_NAME,
            aws_access_key_id=settings.S3_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_AWS_SECRET_ACCESS_KEY,
        )

        try:
            image_binary = base64.b64decode(image)
        except binascii.Error:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=messages.IMAGE_BASE64_NOT_VALID)

        s3_client.Object(settings.BUCKET, path).put(Body=image_binary, ContentType="image/jpeg")
