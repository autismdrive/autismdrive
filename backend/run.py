from app.main import app
import os

port = int(os.environ.get("FLASK_RUN_PORT", 5000))

print("Running on port " + str(port))
app.run(host="0.0.0.0", threaded=True, port=port)
app.schedule_tasks()
