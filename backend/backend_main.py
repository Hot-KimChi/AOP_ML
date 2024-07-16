import configparser
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from pkg_SQL.database import SQL
from pkg_MeasSetGen.meas_generation import MeasSetGen
from pkg_Viewer.viewer import Viewer
from pkg_Verify_Report.verify_report import Verify_Report
from pkg_MachineLearning.machine_learning import Machine_Learning

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def process_file(file_path):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    processed_data = {"original_content": data, "length": len(data)}
    return processed_data


def load_config():
    config_path = os.path.join(".", "backend", "AOP_config.cfg")
    config = configparser.ConfigParser()
    config.read(config_path)

    for section, options in config.items():
        for key, value in options.items():
            os.environ[f"{section.upper()}_{key.upper()}"] = value


def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Error occurred: {str(e)}", exc_info=True)
            return jsonify({"status": "error", "message": str(e)}), 500

    return decorated_function


@app.route("/process-file", methods=["POST"])
@handle_exceptions
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
        return jsonify({"status": "success", "data": processed_data})


@app.route("/api/get_databases", methods=["GET"])
@handle_exceptions
def get_databases():
    databases = os.environ.get("DATABASE_NAME", "").split(",")
    return jsonify({"status": "success", "data": databases})


@app.route("/api/meas_generation", methods=["POST"])
@handle_exceptions
def meas_generation():
    data = request.json
    database = data.get("database")
    list_probe = data.get("list_probe")

    probe_list = list_probe.split("\n") if isinstance(list_probe, str) else list_probe

    meas_gen = MeasSetGen(database, probe_list)
    result = meas_gen.generate()

    return jsonify({"status": "success", "data": result})


@app.route("/api/verify_report", methods=["POST"])
@handle_exceptions
def verify_report():
    data = request.json
    database = data.get("database")
    list_probe = data.get("list_probe")
    verify_report = Verify_Report(database, list_probe)
    result = verify_report.generate()  # Assuming there's a generate method
    return jsonify({"status": "success", "data": result})


@app.route("/api/machine_learning", methods=["POST"])
@handle_exceptions
def machine_learning():
    data = request.json
    database = data.get("database")
    ml = Machine_Learning(database)
    result = ml.process()  # Assuming there's a process method
    return jsonify({"status": "success", "data": result})


@app.route("/api/get_probeinfo", methods=["GET"])
@handle_exceptions
def get_probeinfo():
    connect = SQL(command=1)
    df = connect.sql_get()
    list_probe = [
        {"probename": str(row[0]), "probeid": str(row[1])} for row in df.values.tolist()
    ]
    return jsonify({"status": "success", "data": list_probe})


if __name__ == "__main__":
    load_config()
    app.run(host="0.0.0.0", port=5000, debug=True)
