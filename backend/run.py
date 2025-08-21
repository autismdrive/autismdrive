from app.api_app import APIApp


print("Loading backend/run.py")
app: APIApp

if __name__ == "__main__":
    import os
    import click
    from app.create_app import create_app

    port = int(os.environ.get("FLASK_RUN_PORT", 5000))

    click.secho("Creating app...")
    app = create_app()

    click.secho("Running on port " + str(port))
    app.run(host="0.0.0.0", threaded=True, port=port)

    click.secho("Scheduling tasks...")
    app.schedule_tasks()
