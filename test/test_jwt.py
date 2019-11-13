import unittest
from datetime import timedelta
from time import sleep

from lib.jwt_utils.jwt_utils import create_access_token, decode_jwt, create_refresh_token


class TestMongoDB(unittest.TestCase):

    def setUp(self):
        ...

    def test_token(self):
        id = 10086
        expires_delta = timedelta(seconds=1)
        token = create_access_token(id, expires_delta)
        refresh_token = create_refresh_token(id, expires_delta)
        # sleep(2)
        print(token)
        print(refresh_token)
        decoded = decode_jwt(token)
        refresh_token = decode_jwt(refresh_token)
        print(decoded)
        print(refresh_token)
        assert decoded['idt'] == id
