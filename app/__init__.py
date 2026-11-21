"""Mini-VulnFinBot application factory."""
import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        MAX_CONTENT_LENGTH=16384,
        AI_BACKEND=os.getenv("AI_BACKEND", "ollama"),
        OLLAMA_URL=os.getenv("OLLAMA_URL", "http://127.0.0.1:11434"),
        OLLAMA_MODEL=os.getenv("OLLAMA_MODEL", "phi3:latest"),
        AI_TIMEOUT=120,
        TESTING=False,
    )
    if config:
        app.config.update(config)
    from app.routes import bp
    app.register_blueprint(bp)

    @app.after_request
    def security_headers(response):
        response.headers.update({
            "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "no-referrer",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
            "Cross-Origin-Embedder-Policy": "require-corp",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cross-Origin-Resource-Policy": "same-origin",
            "Cache-Control": "no-store",
        })
        return response

    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify(error=error.name), error.code

    @app.errorhandler(Exception)
    def unexpected_error(error):
        # Never log prompts, model output, credentials or exception details.
        app.logger.error("Request failed; details suppressed")
        return jsonify(error="Internal server error"), 500

    return app
