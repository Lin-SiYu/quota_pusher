import datetime
import uuid
from calendar import timegm

import jwt

SECRET = 'L1gldh^gxfc5&*(^RFJVHJ@'


def create_access_token(identity, expires_delta=None, fresh=False):
    '''
    :param identity: Identifier for who this token is for (ex, username). This
                     data must be json serializable
    :param secret: Secret key to encode the JWT with
    :param expires_delta: How far in the future this token should expire
                          (set to False to disable expiration)
    :type expires_delta: datetime.timedelta or False
    :param fresh: If this should be a 'fresh' token or not. If a
                  datetime.timedelta is given this will indicate how long this
                  token will remain fresh.
    :return:
    '''
    if isinstance(fresh, datetime.timedelta):
        now = datetime.datetime.utcnow()
        fresh = timegm((now + fresh).utctimetuple())

    token_data = {
        'idt': identity,
        'fresh': fresh,
        'type': 'access',
    }
    access_token = _encode_jwt(token_data, expires_delta=expires_delta)

    # access_token = jwt.encode(token_data, secret, algorithm, json_encoder=json.JSONEncoder).decode('utf-8')
    return access_token


def create_refresh_token(identity, expires_delta=None):
    token_data = {
        'idt': identity,
        'type': 'refresh'
    }

    refresh_token = _encode_jwt(token_data, expires_delta=expires_delta)
    # refresh_token = jwt.encode(token_data, secret, algorithm, json_encoder=json.JSONEncoder).decode('utf-8')
    return refresh_token


def _encode_jwt(additional_token_data, expires_delta, algorithm='HS256', json_encoder=None):
    uid = str(uuid.uuid4())
    now = datetime.datetime.utcnow()
    token_data = {
        'iat': now,
        'nbf': now,
        'jti': uid,
        'exp': now + expires_delta
    }
    token_data.update(additional_token_data)
    encode_token = jwt.encode(token_data, SECRET, algorithm, json_encoder=json_encoder).decode('utf-8')
    # encode_token = jwt.encode(token_data, secret, algorithm, json_encoder=json.JSONEncoder).decode('utf-8')
    return encode_token


def decode_jwt(encoded_token, algorithm='HS256'):
    data = jwt.decode(encoded_token, SECRET, algorithms=[algorithm])
    return data


def get_user_id(encoded_token):
    # 获取 userID
    # 在用户登录时候, idt 赋值为 userID, 方便之后操作
    return decode_jwt(encoded_token).get('idt', None)
