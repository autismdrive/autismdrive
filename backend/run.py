import sys

if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 5000

from app.main import app

print("Running on port " + str(port))
app.run(host="0.0.0.0", threaded=True, port=port)
app.schedule_tasks()
