from flask import Blueprint, current_app, jsonify, render_template, request

from app.ai import INPUT_REFUSAL, ModelUnavailable, call_model, input_is_restricted, validate_output

bp = Blueprint("main", __name__)
MAX_MESSAGE_LENGTH = 2000


@bp.get("/health")
def health():
    return jsonify(status="healthy")


@bp.get("/")
def index():
    return render_template("index.html", backend=current_app.config["AI_BACKEND"], model=current_app.config["OLLAMA_MODEL"])


@bp.post("/api/chat")
def chat():
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Expected a JSON object"), 400
    message = data.get("message")
    if not isinstance(message, str):
        return jsonify(error="message must be a string"), 400
    if not message.strip() or len(message) > MAX_MESSAGE_LENGTH:
        return jsonify(error="message must contain 1–2000 characters"), 400
    if input_is_restricted(message):
        return jsonify(response=INPUT_REFUSAL, backend="policy", model="not-called", safety="blocked")
    try:
        output = call_model(message.strip(), current_app.config)
    except ModelUnavailable:
        return jsonify(error="Model unavailable. Check local Ollama.", backend=current_app.config["AI_BACKEND"]), 503
    reply, blocked = validate_output(output)
    return jsonify(response=reply, backend=current_app.config["AI_BACKEND"], model=current_app.config["OLLAMA_MODEL"] if current_app.config["AI_BACKEND"] == "ollama" else "mock", safety="blocked" if blocked else "validated")
