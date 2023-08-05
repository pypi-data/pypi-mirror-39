import paho.mqtt.client as mqtt
import time
import subprocess
from os import environ as env
import json
from datetime import datetime

def getID():
    x = filter(lambda x : x.startswith('Serial'), subprocess.check_output(['cat','/proc/cpuinfo']).split('\n'))
    if len(x) > 0:
        return x[0].split(':')[1].strip().lstrip('0')
    else:
        return None

localdb = {}
localdbperboard = {}
broadcastdb = None
localfn = {'update':{}, 'change':{}}
boardId = None


def putMessageInDb(topic, msg):
    global broadcastdb, localdb
    if (topic.split('/')[0] == 'broadcast'):
        broadcastdb = msg
    elif (topic.split('/')[0] == 'in'):
        localdb[topic.split('/')[-1]] = msg

        if topic.split('/')[-2] not in localdbperboard:
            localdbperboard[topic.split('/')[-2]] = {}

        localdbperboard[topic.split('/')[-2]][topic.split('/')[-1]] = msg
    



class ArgumentError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(ArgumentError, self).__init__(message)

class EnvironmentError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(EnvironmentError, self).__init__(message)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Wmqtt(object):
    __metaclass__ = Singleton
    def __init__(self):
        self.initVars()
        self.connect()
        self.subscribe()

    def initVars(self):
        global boardId
        if env.has_key('BOARD_ID'):
            self.boardId = env['BOARD_ID']
        else:
            self.boardId = getID()
            if self.boardId == None:
                raise EnvironmentError("Error finding environment variable BOARD_ID")

        boardId = self.boardId

        if env.has_key('BROKER_ADDRESS'):
            self.brokerAddress = env['BROKER_ADDRESS']
        else:
            raise EnvironmentError("Error finding MQTT broker address from environment variable BROKER_ADDRESS")

        print 'Board ID', self.boardId
        print 'Broker address', self.brokerAddress

    
    def form(self, message):
        return json.dumps({'s':self.boardId, 'm':message, 't':datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


    def on_message(self, client, userdata, messagejson):
        loaded = json.loads(str(messagejson.payload.decode('utf-8')))

        #s = loaded['s']
        message = loaded['m']
        #t = loaded['t']

        putMessageInDb(messagejson.topic, message)


    def connect(self):
        self.client = mqtt.Client(self.boardId)
        self.client.on_message=self.on_message
        self.client.connect(self.brokerAddress)

        self.client.loop_start()

    def subscribe(self, topic='default'):
        self.client.subscribe('broadcast')
        self.client.subscribe('in' + '/' + self.boardId + '/' + '+')


    def sendMessage(self,msg,boardId,topic = 'default'):
        self.client.publish('in' + '/' + boardId + '/' + topic, self.form(msg))


    def broadcastMessage(self, msg):
        self.client.publish('broadcast', self.form(msg))


class AwayInfo(object):
    def __init__(self, topic = 'default', board = None):
        self.topic = topic
        self.board = board

    @property
    def valuesBroadcast(self):
        while True:
            if broadcastdb != None:
                yield broadcastdb

    @property
    def values(self):
        if self.board:
            while True:
                if localdbperboard.has_key(self.board) and localdbperboard[self.board].has_key(self.topic):
                    yield localdbperboard[self.board][self.topic]
        else:
            while True:
                if localdb.has_key(self.topic):
                    yield localdb[self.topic]


    def isBroadcastAvailable(self):
        return broadcastdb != None

    def isAvailable(self):
        if self.board:
            return localdb.has_key(self.topic)
        else:
            return localdbperboard.has_key(self.board) and localdbperboard[self.board].has_key(self.topic)

    def getBroadcastAvailable(self):
        if (self.isBroadcastAvailable()):
            return broadcastdb

    def getAvailable(self):
        if (self.isAvailable()):
            if self.board:
                return localdbperboard[self.board][self.topic]
            else:
                return localdb[self.topic]
            



