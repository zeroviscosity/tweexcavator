#!/usr/bin/env python

import unittest
import tweexcavator
import datetime

class TestStatus:
    """Helper class for TweexcavatorTests.test_on_status"""    
    def __init__(self):
        self.id = 1
        self.created_at = datetime.datetime(2013, 1, 1)
        self.text = "testing 123"
        self.author = TestAuthor()

class TestAuthor:
    """Helper class for TweexcavatorTests.test_on_status"""    
    def __init__(self):
        self.name = "Test"
        self.screen_name = "test"

class TweexcavatorTests(unittest.TestCase):
    def setUp(self):
        #Enter your MongoDB info here
        self.db_host = ""
        self.db_name = ""
        self.db_collection = ""

    def test_establish_db_connection(self):
        """Ensure that we have a MongoDB collection after connecting to the
        database."""        
        t = tweexcavator.Tweexcavator()
        t.establish_db_connection(self.db_host, self.db_name, 
            self.db_collection)
        self.assertEqual(str(t.collection.__class__), 
            "<class 'pymongo.collection.Collection'>")
        
    def test_on_status(self):
        """Ensure that the tweets get saved in the database"""        
        t = tweexcavator.Tweexcavator()
        t.establish_db_connection(self.db_host, self.db_name, 
            self.db_collection)
        t.connection.write_concern = {'w': 1}    
        
        status = TestStatus()
        t.on_status(status)
        self.assertNotEqual(t.collection.find_one({"id": status.id}), None)
        t.collection.remove({"id": status.id})
        
if __name__ == '__main__':
    unittest.main()
