import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from .database import Base, engine

# Song is the parent to a file, with a one to one relationship

class Song(Base): 
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    file = relationship("File", uselist=False, backref="song")

    # The song as dictionary method should produce a dictionary that looks like: 
    """
    {
        "id": 1,
        "file": {
            "id": 7,
            "name": "Shady_Grove.mp3"
        }
    }
    """
    
    def as_dictionary(self):
        song = {
            "id": self.id,
            "file": self.file.as_dictionary()
        }
        return song

# File contains the foreign key for song id

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    filename = Column(String(128))
    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)
    
    # The file as dictionary method should produce a dictionary that looks like: 
    """
    {"id": 7, "name": "Shady_Grove.mp3"}
    """
    
    def as_dictionary(self):
        file = {
            "id": self.id,
            "filename": self.filename,
        }
        return file