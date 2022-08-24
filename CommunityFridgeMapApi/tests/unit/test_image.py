import pytest
import base64
from unittest.mock import patch, ANY
from functions.image.v1.app import ImageHandler
from tests.assert_resposne import assert_response


def test_upload(storage_stub):
    blob = b'123123123'
    b64encoded_blob = base64.b64encode(blob).decode("ascii")
    with patch.object(storage_stub, "write", wraps=storage_stub.write) as write_spy:
        response = ImageHandler.upload_handler(
            event={
                "isBase64Encoded": True,
                "body": b64encoded_blob,
            },
            storage=storage_stub
        )
        write_spy.assert_called_once_with(ANY, blob)
        assert_response(
            response,
            status=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            body={
                "bucket": ANY,
                "key": ANY
            }
        )

def test_download(storage_stub):
    bucket = "fridge-report"
    blob = b"12312312"
    expected_body = base64.b64encode(blob)
    key = storage_stub.write(bucket, blob)
    response = ImageHandler.download_handler(
        event={
            "pathParameters": {
                "bucket": bucket,
                "key": key,
            }
        },
        storage=storage_stub,
    )

    assert_response(
        response,
        status=200,
        headers={
            "Content-Type": "image/webp",
            "Access-Control-Allow-Origin": "*",
        },
        body=expected_body,
    )
