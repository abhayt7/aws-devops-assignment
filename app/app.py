from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from CI/CD on EKS! Version 1"

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
