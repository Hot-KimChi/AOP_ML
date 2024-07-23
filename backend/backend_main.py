import configparser
import os
import getpass
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from functools import wraps
from pkg_SQL.database import SQL
from pkg_MeasSetGen.meas_generation import MeasSetGen
from pkg_Viewer.viewer import Viewer
from pkg_Verify_Report.verify_report import Verify_Report
from pkg_MachineLearning.machine_learning import Machine_Learning
import win32api, win32security

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    resources={
        r"/api/*": {"origins": ["http://localhost:3000", "http://10.82.216.206:3000"]}
    },
)

UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)  # 세션을 위한 시크릿 키 설정
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True


def load_config():
    config_path = os.path.join(".", "backend", "AOP_config.cfg")
    config = configparser.ConfigParser()
    config.read(config_path)

    for section in config.sections():
        for key, value in config[section].items():
            # 섹션 이름과 키에서 공백 제거 및 대문자 변환
            env_var_name = (
                f"{section.replace(' ', '_').upper()}_{key.replace(' ', '_').upper()}"
            )
            os.environ[env_var_name] = value

    # 데이터베이스 이름은 쉼표로 구분된 리스트이므로 별도 처리
    if "database" in config and "name" in config["database"]:
        os.environ["DATABASE_NAME"] = config["database"]["name"]


def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Error occurred: {str(e)}", exc_info=True)
            return jsonify({"status": "error", "message": str(e)}), 500

    return decorated_function


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "authenticated" not in session or not session["authenticated"]:
            return (
                jsonify({"status": "error", "message": "Authentication required"}),
                401,
            )
        return f(*args, **kwargs)

    return decorated_function


@app.route("/api/authenticate", methods=["POST"])
@handle_exceptions
def authenticate():
    user = getpass.getuser()
    try:
        # MSSQL 서버에 연결 시도
        connect = SQL(windows_auth=True)
        # 연결 성공 시 세션에 인증 정보 저장
        session["authenticated"] = True
        session["user"] = user
        session.permanent = True  # 세션을 영구적으로 유지
        return jsonify({"status": "success", "authenticated": True, "user": user})
    except Exception as e:
        # 연결 실패 시
        return (
            jsonify({"status": "error", "authenticated": False, "message": str(e)}),
            401,
        )


@app.route("/api/get_windows_user", methods=["GET"])
@handle_exceptions
def get_windows_user():
    if "authenticated" in session and session["authenticated"]:
        user = session["user"]
        try:
            # 사용자의 전체 이름(Full Name) 가져오기
            sid = win32security.LookupAccountName(None, user)[0]
            full_name = win32api.GetUserNameEx(win32api.NameDisplay)
            return jsonify(
                {
                    "status": "success",
                    "authenticated": True,
                    "user": user,
                    "full_name": full_name,
                    "connection_status": "연결 완료",
                }
            )
        except Exception as e:
            return jsonify(
                {
                    "status": "error",
                    "authenticated": True,
                    "user": user,
                    "connection_status": "Admin 문의",
                    "message": f"Full name retrieval failed: {str(e)}",
                }
            )
    else:
        return (
            jsonify(
                {
                    "status": "error",
                    "authenticated": False,
                    "message": "Not authenticated",
                }
            ),
            401,
        )


@app.route("/api/get_databases", methods=["GET"])
@handle_exceptions
@require_auth
def get_databases():
    databases = os.environ.get("DATABASE_NAME", "").split(",")
    return jsonify({"status": "success", "data": databases})


@app.route("/api/process-file", methods=["POST"])
@handle_exceptions
@require_auth
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


@app.route("/api/meas_generation", methods=["POST"])
@handle_exceptions
@require_auth
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
@require_auth
def verify_report():
    data = request.json
    database = data.get("database")
    list_probe = data.get("list_probe")
    verify_report = Verify_Report(database, list_probe)
    result = verify_report.generate()
    return jsonify({"status": "success", "data": result})


@app.route("/api/machine_learning", methods=["POST"])
@handle_exceptions
@require_auth
def machine_learning():
    data = request.json
    database = data.get("database")
    ml = Machine_Learning(database)
    result = ml.process()
    return jsonify({"status": "success", "data": result})


@app.route("/api/get_probeinfo", methods=["GET"])
@handle_exceptions
@require_auth
def get_probeinfo():
    connect = SQL(command=1)
    df = connect.sql_get()
    list_probe = [
        {"probename": str(row[0]), "probeid": str(row[1])} for row in df.values.tolist()
    ]
    return jsonify({"status": "success", "data": list_probe})


def process_file(file_path):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    processed_data = {"original_content": data, "length": len(data)}
    return processed_data


if __name__ == "__main__":
    load_config()
    app.run(host="0.0.0.0", port=5000, debug=True)
