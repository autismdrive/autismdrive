from app.api_app import APIApp
from app.create_app import create_app
import dotenv
import os

print("Loading backend/run.py")

app: APIApp

if __name__ == "__main__":
    print("Running backend/run.py")

    # Load all environment variables from .env file
    dotenv.load_dotenv(dotenv_path=".env")

    port = int(os.environ.get("FLASK_RUN_PORT", 5000))

    print("Running on port " + str(port))
    app = create_app()
    app.run(host="0.0.0.0", threaded=True, port=port)
    app.schedule_tasks()
