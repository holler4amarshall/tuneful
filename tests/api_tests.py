import unittest
import os
import shutil
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO

import sys; print(list(sys.modules.keys()))
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())
        
        
    def test_get_empty_list_of_songs(self):
        """ Getting songs - fail: DB empty"""
        #No Song Data is added to DB
        #query api
        response = self.client.get("/api/songs",
        headers=[("Accept", "application/json")]
        )
        #assert api response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data, [])
        
       
    def test_get_songs(self):
        """ Getting songs - success """
        #Add 2 Songs to DB with File Data
        file1 = models.File(filename="Awake.mp3")
        file2 = models.File(filename="Montana.mp3")
        song1 = models.Song(name="Awake", file=file1)
        song2 = models.Song(name="Montana", file=file2)
        
        session.add_all([song1, song2])
        session.commit()
        
        #query api
        response = self.client.get("/api/songs")
        print(response)
        
        #assert api response contains expected response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(data), 2)
        
        #assert response contains expected songs/file
        song1 = data[0]
        print(song1)
        self.assertEqual(song1["songname"], "Awake")
        self.assertEqual(song1["file"]["filename"], "Awake.mp3")
        self.assertEqual(song1["file"]["id"], song1["id"])

        song2 = data[1]
        self.assertEqual(song2["songname"], "Montana")
        self.assertEqual(song2["file"]["filename"], "Montana.mp3")
        self.assertEqual(song1["file"]["id"], song2["id"])

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())


