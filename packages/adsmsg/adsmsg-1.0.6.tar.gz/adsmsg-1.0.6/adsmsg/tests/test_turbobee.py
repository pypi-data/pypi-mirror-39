import sys
import os

import unittest
from adsmsg import TurboBeeMsg, Status
from datetime import datetime

class TestTurboBee(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.proj_home = os.path.join(os.path.dirname(__file__), '../..')


    def tearDown(self):
        unittest.TestCase.tearDown(self)


    def test_is_valid(self):
        rec = TurboBeeMsg()
        rec.qid = 'foo'
        self.assertTrue(rec.is_valid())
        
        rec.qid = 'unlimiteeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeed' * 512
        self.assertTrue(rec.is_valid())
        
        rec.status = Status.new
        now = datetime.utcnow()
        
        rec.created = rec.get_timestamp(now)
        self.assertEqual(now, rec.get_datetime(rec.created))
        
        rec.value = 'foobar'
        rec.ctype = rec.ContentType.text
        rec.ctype = 0 # unknown
        self.assertTrue(rec.is_valid())
        
        rec.set_value(1)
        self.assertTrue(rec.is_valid())    
    
        rec.set_value(u'\ud789')
        rec.ctype = rec.ContentType.text
        
        self.assertEqual(rec.get_value(), u'\ud789'.encode('utf8'))
        rec.ctype = rec.ContentType.binary
        self.assertEqual(rec.get_value(), u'\ud789'.encode('utf8'))
        
        rec.set_value({'foo': u'\ud789'}, rec.ContentType.json)
        self.assertEqual(rec.get_value(), {'foo': u'\ud789'})
        
        rec.set_value(u'\ud789', rec.ContentType.text)
        self.assertEqual(rec.get_value(), u'\ud789'.encode('utf8'))
        

    def test_serializer(self):
        # check we are not movng dates (by loosing nanosec precision)
        rec = TurboBeeMsg()
        now = datetime.utcnow()
        rec.created = rec.get_timestamp(now)
        
        for i in xrange(10050):
            rec = rec.loads(*rec.dump())
            self.assertEqual(rec.get_datetime(rec.created), now)
        

if __name__ == '__main__':
    unittest.main()
