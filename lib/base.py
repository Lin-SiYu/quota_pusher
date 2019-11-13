import json
import traceback

from tornado.options import options
from tornado.web import RequestHandler, HTTPError

from app import errors
from app.errors import HTTPAPIError
from app.handlers.response_handler import ResponseHandler
from lib.log import logger_error
from lib.mail.wymail import send_mail


class APIHandler(RequestHandler, ResponseHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers",
                        "Authorization,Accept,Origin,User-Agent,x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, DELETE, PUT, OPTIONS')

    def prepare(self):
        params = dict()
        params['Referer'] = self.request.headers.get('Referer', '')
        params['Cookie'] = self.request.headers.get('Cookie', '')
        params['User-Agent'] = self.request.headers.get('User-Agent', '')

        # todo auth role
        pass

    def options(self):
        # auth
        self.set_status(204)
        self.finish()

    def format_param_get(self, dict_list):
        for key in dict_list:
            try:
                dict_list[key] = json.loads(dict_list[key])
            except:
                continue

        return dict_list

    def write_error(self, status_code, **kwargs):
        msg = ''
        # override
        debug = options.DEBUG
        self.set_status(status_code)  # always return 200 OK for API errors
        try:
            exc_info = kwargs.pop('exc_info')
            e = exc_info[1]
            logger_error.error('status_code %d' % status_code)
            if isinstance(e, HTTPAPIError):
                msg = str(e)
            elif isinstance(e, HTTPError):
                self.set_status(status_code)
            else:
                # for unknown error
                e = HTTPAPIError(10001)
                msg = str(e)

            exception = "".join([ln for ln in traceback.format_exception(*exc_info)])

            logger_error.error(exception)

            if status_code == 500 and not debug:
                self._send_error_email(exception)

            if debug:
                if status_code == 200:
                    e.response["exception"] = exception
                msg = str(e)

            # self.clear()
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.finish(msg)
        except:
            logger_error.error(traceback.format_exc())
            return super(APIHandler, self).write_error(status_code, **kwargs)

    def _send_error_email(self, exception):
        try:
            subject = "[%s]Internal Server Error" % options.SITE_NAME
            body = exception
            if options.SEND_MAIL:
                send_mail(options.MAIL_LIST, subject, body)
                # todo mail sender should be async
        except:
            logger_error.error(traceback.format_exc())

    @property
    def redis(self):
        return self.application.redis

    @property
    def db(self):
        return self.application.db


class APIErrorHandler(APIHandler):
    def prepare(self):
        super(APIErrorHandler, self).prepare()
        raise errors.HTTPAPIError(404, status_code=404)
