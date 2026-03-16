from flask import Flask, request, jsonify
import zipfile
import io
import base64

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_zip():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        if "fileContent" not in data:
            return jsonify({"error": "fileContent is missing"}), 400

        if "fileName" not in data:
            return jsonify({"error": "fileName is missing"}), 400

        file_name = data["fileName"]
        file_content_base64 = data["fileContent"]

        zip_bytes = base64.b64decode(file_content_base64)
        zip_file = io.BytesIO(zip_bytes)

        password = b"12345678"

        with zipfile.ZipFile(zip_file) as z:
            for name in z.namelist():
                if name.lower().endswith(".txt"):
                    content = z.read(name, pwd=password)
                    text = content.decode("utf-8", errors="ignore")

                    return jsonify({
                        "zipFileName": file_name,
                        "txtFileName": name,
                        "content": text
                    })

        return jsonify({"error": "No TXT inside ZIP"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "API activa", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
