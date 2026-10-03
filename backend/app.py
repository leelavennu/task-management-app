import os
from datetime import datetime, timezone
from flask import Flask, jsonify
from flask_cors import CORS
from pydantic import ValidationError
from models import db
from routes import tasks_bp

def create_app(test_config=None):
    app = Flask(__name__)
    database_url = os.getenv("DATABASE_URL", "sqlite:///tasks.db")
    app.config.update(SQLALCHEMY_DATABASE_URI=database_url, SQLALCHEMY_TRACK_MODIFICATIONS=False)
    if test_config: app.config.update(test_config)
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(tasks_bp, url_prefix="/api")
    @app.errorhandler(400)
    def bad_request(error): return jsonify(error="Bad request", message=getattr(error, "description", "Malformed request")), 400
    @app.errorhandler(500)
    def server_error(error): return jsonify(error="Server error", message="Something went wrong. Please retry."), 500
    with app.app_context(): db.create_all()
    return app

app = create_app()
if __name__ == "__main__": app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
