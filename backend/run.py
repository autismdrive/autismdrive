from app.main import app
import dotenv
import os

# Load all environment variables from .env file
dotenv.load_dotenv(dotenv_path=".env")

port = int(os.environ.get("FLASK_RUN_PORT", 5000))

print("Running on port " + str(port))
app.run(host="0.0.0.0", threaded=True, port=port)
app.schedule_tasks()
