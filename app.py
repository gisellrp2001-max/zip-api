from flask import Flask, request, jsonify
import zipfile

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_zip():

    if 'file' not in request.files:
        return jsonify({"error": "No file received"}), 400

    file = request.files['file']
    password = b'12345678'

    try:
        with zipfile.ZipFile(file) as z:
            for name in z.namelist():
                if name.endswith(".txt"):
                    content = z.read(name, pwd=password)
                    text = content.decode("utf-8", errors="ignore")

                    return jsonify({
                        "file": name,
                        "content": text
                    })

        return jsonify({"error": "No TXT inside ZIP"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)