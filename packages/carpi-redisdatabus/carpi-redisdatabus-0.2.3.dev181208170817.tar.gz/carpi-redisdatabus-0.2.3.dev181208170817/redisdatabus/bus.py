"""
CARPI REDIS DATA BUS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
from logging import Logger
from threading import Thread
from time import sleep, time
from typing import Any

from carpicommons.log import logger
from redis import StrictRedis
from redis.client import PubSub


class BusWriter(object):
    def __init__(self,
                 redis: StrictRedis=None,
                 host: str='127.0.0.1',
                 port: int=6379,
                 db: int=0,
                 password: str=None):
        """
        Instantiates a new Bus Writer.
        You can either pass an existing Redis instance or
        initialize a new Redis instance by providing host, port,
        db and password
        :param redis: An already initialized Redis instance
        :param host: Redis host
        :param port: Redis host port
        :param db: Redis database
        :param password: Redis password
        """
        self._log: Logger = logger(self.__class__.__name__)
        log = self._log
        if redis:
            self._r = redis
            log.info("Initialized a new Bus Writer from a given Redis instance")
        else:
            self._r = StrictRedis(host=host,
                                  port=port,
                                  db=db,
                                  password=password)
            log.info("Initialized a new Bus Writer on redis://{}:{}/{}".format(host, port, db))

    def publish(self, channel: str, value: Any):
        """
        Sends a new value to the data bus
        :param channel: Defines the name of the value
        :param value: Defines the value itself
        """
        self._r.publish(channel, str(value))


class BusListener(Thread):
    def __init__(self,
                 channels: list,
                 name: str=None,
                 redis: StrictRedis=None,
                 host: str='127.0.0.1',
                 port: int=6379,
                 db: int=0,
                 password: str=None):
        """
        :param channels: List of channels this BusListener listens on
        :param name:
        :param redis:
        :param host:
        :param port:
        :param db:
        :param password:
        """
        Thread.__init__(self)

        self._log: Logger = logger(self.__class__.__name__)
        log = self._log

        if redis:
            self._r = redis
        else:
            self._r = StrictRedis(host=host,
                                  port=port,
                                  db=db,
                                  password=password)
            log.info("Initialized a new Bus Listener on redis://{}:{}/{}".format(host, port, db))

        self.setName(name
                     if name
                     else "{}{:.0f}".format(self.__class__.__name__, time()))

        self._channels = channels
        self._current_data = {}
        self._callbacks = {}
        self._global_callbacks = []

        log.info("A new {} has been initialized".format(self.__class__.__name__))
        self._running = False

    def _init_listener(self) -> PubSub:
        sub = self._r.pubsub()
        sub.subscribe(self._channels)
        return sub

    def _process_entry(self, msg: dict) -> (str, Any):
        return msg['channel'].decode('utf-8'), \
               msg['data'].decode('utf-8')

    def register_global_callback(self, callback):
        self._global_callbacks.append(callback)

    def register_channel_callback(self, channel, callback):
        if channel not in self._callbacks:
            self._callbacks[channel] = []
        self._callbacks[channel].append(callback)

    def run(self) -> None:
        self._log.info("Starting up...")
        self._running = True

        sub = self._init_listener()
        while self._running:
            msg = sub.get_message(ignore_subscribe_messages=True,
                                  timeout=1)
            if msg and msg['type'] == 'message':
                channel, data = self._process_entry(msg)

                self._log.info('{}: {}'.format(channel, data))
                self._current_data[channel] = data
                for glc in self._global_callbacks:
                    glc(channel, data)
                if channel in self._callbacks:
                    for cl in self._callbacks[channel]:
                        cl(channel, data)
            sleep(0.001)

    def stop(self):
        self._running = False
        self.join()


class TypedBusListener(BusListener):
    TYPE_PREFIX_STRING = "s#"
    TYPE_PREFIX_INT = "i#"
    TYPE_PREFIX_FLOAT = "f#"
    TYPE_PREFIX_BOOL = "b#"

    def __init__(self,
                 channels: list,
                 name: str=None,
                 redis: StrictRedis=None,
                 host: str='127.0.0.1',
                 port: int=6379,
                 db: int=0,
                 password: str=None):
        BusListener.__init__(self, channels, name, redis,
                             host, port, db, password)

    def _process_entry(self, msg: dict) -> (str, Any):
        channel, message = BusListener._process_entry(self, msg)  # type: str, str

        if channel.startswith(TypedBusListener.TYPE_PREFIX_INT):
            try:
                message = int(message)
            except ValueError:
                message = None
        elif channel.startswith(TypedBusListener.TYPE_PREFIX_FLOAT):
            try:
                message = float(message)
            except ValueError:
                message = None
        elif channel.startswith(TypedBusListener.TYPE_PREFIX_BOOL):
            message = message == "1"

        return channel, message


if __name__ == "__main__":
    print("This script is not intended to be run standalone!")
