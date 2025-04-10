from app.create_app import create_app

app = create_app()

# uwsgi automatically looks for a callable called "application"
application = app
