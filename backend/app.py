from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
from flask_cors import CORS  # 추가

app = Flask(__name__)
CORS(app)  # CORS 허용
UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def process_file(file_path):
    # 파일 처리 로직 (예시로 간단하게 처리)
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    processed_data = {"original_content": data, "length": len(data)}
    return processed_data


@app.route("/process-file", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        processed_data = process_file(file_path)
        return jsonify(processed_data)


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host="0.0.0.0", port=5000)
