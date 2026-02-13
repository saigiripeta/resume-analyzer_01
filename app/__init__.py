from flask import Flask
from pathlib import Path

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object("app.config.Config")

    # Ensure uploads directory exists
    upload_dir = Path(app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Register routes
    from .main import main_bp
    app.register_blueprint(main_bp)

    return app

