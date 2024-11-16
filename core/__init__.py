import os
from flask import Flask

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "core", "static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
from core import routes
