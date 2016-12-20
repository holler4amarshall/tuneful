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
    # Get the querystring arguments
    #name_like = request.args.get("name_like")

    # Get and filter the songs from the database
    songs = session.query(models.Song)
    #if name_like:
    #    songs = songs.filter(models.Song.name.contains(name_like))
    songs = songs.order_by(models.Song.id)

    # Convert the posts to JSON and return a response
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")


