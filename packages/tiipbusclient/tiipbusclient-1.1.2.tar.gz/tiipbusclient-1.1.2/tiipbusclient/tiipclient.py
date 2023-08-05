"""
    Client for communication over redis in the TIIP protocol
"""
from pytiip.tiip import TIIPMessage
import redis
from queue import Queue, Empty
from threading import Thread

__status__ = 'Development'
import uuid
import time


class ThreadedTiipCallback:
    """
        A callback object, for use with the client, that spawns a thread to run the target function with a TIIPMessage
    """

    def __init__(self, target):
        """
        Construct a callback object, for use with the client, that uses the target function
        :param target: The function to execute when running the Callback. The function should take a TIIPMessage as argument and return a TIIPMessage as return value
        """
        self.target = target

    def __call__(self, *args, **kwargs):
        self.call(args[0], None)

    def call(self, msg, client):
        """
        The call function that executes the target function.
        :param message: a TIIPMessage to send as an argument to the target function
        :param client: Not used for backwards compability only
        :return: None (the reply needs to be handled in the target function)
        """
        message = TIIPMessage(msg["data"])
        if message.type == "pub" and message.ch.startswith("pub/"):
            message.ch = message.ch[4:]

        Thread(target=self.target, args=[message], daemon=True).start()


class TiipClient:
    """
    A TIIPMessage aware bus communication client
    """

    DefaultTimeout = 30

    def __init__(self, clientId, port=6379, addr="localhost"):
        if addr.startswith("ff01"):
            addr = "localhost"
        self.addr = addr
        self.port = port
        self.clientId = clientId
        self.closing = False
        self.__registeredBusInterfaces = list()
        self.requestQueues = dict()
        self.subscriptions = {}

        try:
            self.r = redis.StrictRedis(host=self.addr, port=self.port)
            self.p = self.r.pubsub()
            self.subscriptions["rep/" + clientId] = self._handleReply
            self.p.subscribe(**{"rep/" + clientId: self._handleReply})
        except:
            raise Exception("Redis not Available")
        t = Thread(target=self.run, daemon=True)
        t.start()

    def reconnect(self):
        while not self.closing:
            try:
                self.r = redis.StrictRedis(host=self.addr, port=self.port)
                self.p = self.r.pubsub()

                for chan, cb in self.subscriptions.items():
                    self.p.subscribe(**{chan: cb})
                break
            except:
                time.sleep(1)

    def run(self):
        while not self.closing:
            try:
                frame = self.p.get_message(True, 5.0)
                if not frame:
                    continue
            except:
                self.reconnect()

    def __prepMessage(self, message):
        if message.src:
            if not message.src[-1] == self.clientId:
                message.src.append(self.clientId)
        else:
            message.src = [self.clientId]

    def publish(self, message):
        """
        Publish a TIIPMessage to the channel indicated by message.ch

        :param message: A TIIPMessage object (require the "ch" argument)
        :return: None
        """
        message.type = "pub"
        self.__prepMessage(message)

        self.r.publish('pub/' + message.ch, str(message))

    def reply(self, request, reply):
        """
        Sends a reply to the request sender (request.targ) with the reply.

        :param request: The request (TIIPMessage) to reply to
        :param reply: The reply message (TIIPMessage) to send ("mid" and "sig" is copied from request)
        :return: None
        """
        reply.mid = request.mid
        reply.sig = request.sig
        self.__prepMessage(reply)
        self.r.publish('rep/' + request.src[-1], str(reply))

    def unsubscribe(self, channel):
        """
        Stop subscribing to messages on this channel.

        :param channel: The channel to stop subscribing to
        :return: None
        """
        self.subscriptions.pop(channel)
        self.p.unsubscribe(channel)

    def _handleReply(self, *args, **kwargs):
        """
        Internal function for handling reply callbacks notifying the waiting request thread

        :param args: dynamic arguments with the first being the redis message dict
        :param kwargs: Not Used
        :return:
        """
        tiipMsg = TIIPMessage(args[0]["data"])
        if tiipMsg.mid in self.requestQueues:
            self.requestQueues[tiipMsg.mid].put_nowait(tiipMsg)

    def close(self):
        """
        Terminate all used client resources

        :return: None
        """
        if self.closing:
            return
        self.closing = True
        if self.p:
            self.p.close()

    def request(self, message, timeout=None, retry=None):
        """
        Send a request (TIIPMessage) to the message.targ for the message.sig interface with args in message.arg
        Blocks until a message is received or all attempts have timed out

        :param message: The request (TIIPMessage) to send (requires: targ, sig )
        :param timeout: The timeout per attempt
        :param retry: Amounts of retries on request timeouts
        :return: The reply (TIIPMessage) or None if Timeout
        """
        if message.src:
            if not message.src[-1] == self.clientId:
                message.src.append(self.clientId)
        else:
            message.src = [self.clientId]

        if not message.mid:
            message.mid = uuid.uuid4().hex

        timeout = timeout if timeout else TiipClient.DefaultTimeout

        self.requestQueues[message.mid] = Queue(1)
        doretry = int(retry) if retry else 0
        try:
            for x in range(doretry + 1):
                self.r.publish("req/" + "/".join(message.targ) + "/" + message.sig, str(message))
                try:
                    return self.requestQueues[message.mid].get(True, timeout)
                except Empty:
                    pass
        finally:
            self.requestQueues.pop(message.mid)

    def subscribe(self, channel, callback):
        """
        Register a callback to handle subscriptions to the given channel

        :param channel: The channel on the bus to subscribe to
        :param callback: A callable which take a TIIPMessage as argument
        :return: None
        """
        if isinstance(callback, ThreadedTiipCallback):
            cb = callback
        else:
            cb = ThreadedTiipCallback(callback)

        self.subscriptions["pub/" + channel] = cb
        self.p.subscribe(**{"pub/" + channel: cb})

    def registerBusInterface(self, signal, callback, threaded=True):
        """
        Register an API function which receives TIIPMessage requests and replies on this client with a TIIPMessage reply

        :param signal: The API function name to receive requests for
        :param callback: The callable that takes the request and replies on this client with a TIIPMessage reply
        :param threaded: Not Used @Deprecated
        :return: None
        """
        self.__registeredBusInterfaces.append(signal)

        if isinstance(callback, ThreadedTiipCallback):
            cb = callback
        else:
            cb = ThreadedTiipCallback(callback)

        self.subscriptions["req/" + self.clientId + "/" + signal] = cb
        self.p.subscribe(**{"req/" + self.clientId + "/" + signal: cb})

    def unregisterBusInterface(self, signal):
        """
        Remove a registered API Function

        :param signal: the API function to stop providing.
        :return: None
        """
        self.__registeredBusInterfaces.remove(signal)
        self.unsubscribe("req/" + self.clientId + "/" + signal)

    def getClosed(self):
        return self.closing
