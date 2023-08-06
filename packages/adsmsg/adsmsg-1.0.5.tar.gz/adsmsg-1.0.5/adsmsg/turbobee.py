from .msg import Msg
from .protobuf import turbobee_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
from collections import namedtuple
import json

# helper for access attributes
#ContentTypes = namedtuple('turbobee_CType', turbobee_pb2.TurboBeeMsg.CType.keys())
ContentTypes = namedtuple('CType', [])
for k,v in turbobee_pb2.TurboBeeMsg.CType.items():
    setattr(ContentTypes, k, v)


class TurboBeeMsg(Msg):

    def __init__(self, *args, **kwargs):
        super(TurboBeeMsg, self).__init__(turbobee_pb2.TurboBeeMsg(), args, kwargs)

    @property
    def ContentType(self):
        return ContentTypes
    
    # TODO: maybe I should add smart @property getters/setters for timestamps instead
    
    def get_timestamp(self, dt=None):
        """Makes timestamp out of a datatime (or returns timestamp
        for current time)""" 
        ts = Timestamp()
        if dt:
            ts.FromDatetime(dt)
        else:
            ts.FromDatetime(datetime.utcnow())
        return ts
    
    def get_datetime(self, ts):
        """Turns timestamp into a python datetime.
        Python doesn't have nanoseconds (we are going
        to loose precision). The returned datetime
        is always UTC. """
        
        return datetime.utcfromtimestamp(ts.seconds).replace(microsecond=ts.nanos/1000)
    
    def set_value(self, value, ctype=None):
        """Always sets the value as utf8 encoded bytes"""
        if ctype:
            self.ctype = ctype
        
        # we can only deal with bytes
        if isinstance(value, unicode):
            value = value.encode('utf8')
                
        if self.ctype == ContentTypes.json:
            if not isinstance(value, basestring):
                self.value = json.dumps(value)
        else:
            self.value = bytes(value)
        
        


    def get_value(self):
        """Based on the content type, return property 
        assembled value.
            text: -> utf8 encoded string
            json: -> value loaded by calling json.loads()
            html: -> utf8 encoded string
            all the rest: returns bytes
        """
        if self.ctype == ContentTypes.text or \
            self.ctype == ContentTypes.html:
            return self.value
        elif self.ctype == ContentTypes.json:
            return json.loads(self.value)
        else:
            return self.value
        