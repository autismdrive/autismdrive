"""
Required for uwsgi and the Flask CLI to run the app. The FLASK_APP environment variable must point to the path of this file.
"""

from app.create_app import create_app

app = create_app()

# uwsgi automatically looks for a callable called "application"
application = app
