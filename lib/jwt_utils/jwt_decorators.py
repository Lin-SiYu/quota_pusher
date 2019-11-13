import functools
from _ctypes_test import func

import jwt
from tornado.options import options

from .jwt_utils import decode_jwt


def jwt_required(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):

        res_data = {}
        token = self.request.headers.get('token', None)

        if token:
            try:
                token_data = decode_jwt(token,
                                        options.COOKIE_SECRET)

                user_id = token_data['idt']

                # todo 从 mysql 获取是否有有用户
                # todo 校验 token 是否过期

                # self._current_user = user
                result = await func(self, *args, **kwargs)
                return result
            except jwt.ExpiredSignature:
                self.set_status(401)
                res_data['msg'] = 'Token 已过期'
            except jwt.InvalidTokenError or jwt.InvalidSignatureError:
                self.set_status(403)
                res_data['msg'] = 'Token 非法'
            except:
                # todo 增加查询 user 信息或者 redis 等其他判断
                self.set_status(401)
                # res_data['msg'] = ''
        else:
            self.set_status(401)
            res_data['msg'] = '缺少 Token'
        self.write(res_data)
        # self.finish({})

    return wrapper
