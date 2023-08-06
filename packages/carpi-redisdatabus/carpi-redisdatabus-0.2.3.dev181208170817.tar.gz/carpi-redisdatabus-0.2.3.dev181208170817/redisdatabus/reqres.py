"""
CARPI REDIS DATA BUS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from datetime import datetime, timedelta
from typing import Union

from redis import StrictRedis

from redisdatabus.bus import BusListener, BusWriter
import json


class RequestTimeoutError(Exception):
    def __init__(self, request_name: str):
        super().__init__("Request {} timed out".format(request_name))


class ReqResObject(object):
    def to_json(self) -> str:
        return json.dumps(self,
                          default=lambda i: i.__dict__,
                          sort_keys=True)

    @staticmethod
    def from_json(s: str):
        return json.loads(s)


class RequestObject(ReqResObject):
    pass


class ResponseObject(ReqResObject):
    pass


class RequestListener(BusListener):
    def __init__(self,
                 channels: list,
                 name: str = None,
                 redis: StrictRedis = None,
                 host: str = '127.0.0.1',
                 port: int = 6379,
                 db: int = 0,
                 password: str = None):
        super().__init__(channels,
                         name, redis,
                         host, port, db, password)


class RequestWriter(BusWriter):
    def __init__(self,
                 redis: StrictRedis = None,
                 host: str = '127.0.0.1',
                 port: int = 6379,
                 db: int = 0,
                 password: str = None,
                 timeout: float = 5.0):
        super().__init__(redis,
                         host, port, db, password)
        self._timeout = timeout

    def _wait_for_response(self,
                           request_name: str):
        r = self._r
        s = r.pubsub()
        s.subscribe('res#{}'.format(request_name))

        started_time = datetime.now()
        now_time = datetime.now()
        self._log.debug('Waiting for response for {}'.format(request_name))
        while (now_time - started_time) < timedelta(seconds=self._timeout):
            msg = s.get_message(ignore_subscribe_messages=True,
                                timeout=self._timeout)
            if msg and msg['type'] == 'message':
                channel, data = msg['channel'].decode('utf-8'), msg['data'].decode('utf-8')
                return ReqResObject.from_json(data)

        raise RequestTimeoutError(request_name)

    def send_request(self,
                     request_name: str,
                     request_params: RequestObject = None) -> Union[ResponseObject, None]:
        name = 'req#{}'.format(request_name)
        self._log.debug('Sending request {}'.format(name))
        params = request_params.to_json() if request_params else '{}'
        self.publish(name, params)
        return self._wait_for_response(request_name)


if __name__ == "__main__":
    print("This script is not intended to be run standalone!")
