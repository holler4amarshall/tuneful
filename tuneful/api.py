import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from tuneful import app
from .database import session
from .utils import upload_path


@app.route("/api/songs", methods=["GET"])
#@decorators.accept("application/json")
def songs_get():
    """ Get a list of songs """

    # Get the songs from the database
    songs = session.query(models.Song)
    # order the songs by ID
    songs = songs.order_by(models.Song.id)
    # Convert the songs to JSON and return a response
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/songs", methods=["POST"])
def songs_post():
    """Post a song using file in DB"""
    
    data = request.json
    
    file = session.query(models.File).get(data['filename']['id'])
        
    song = models.Song(filename=file)
    session.add(song)
    session.commit()
    
    # Return 201 response (created) and the full json response
    data = json.dumps(song.as_dictionary())
    headers = {"Location": url_for("songs_get", id=song.id)}
    return Response(data, 200, headers=headers,
                mimetype="application/json")
                
                
"""              
def posts_post():
    """ Add a new post """
    data = request.json

    # Check that the JSON supplied is valid
    # If not you return a 422 Unprocessable Entity
    try:
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    # Add the post to the database
    post = models.Post(title=data["title"], body=data["body"])
    session.add(post)
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")
                    """

