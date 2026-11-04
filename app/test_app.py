from app import app

def test_home():
    assert app.test_client().get("/").status_code == 200

def test_health():
    assert app.test_client().get("/health").data == b"ok"
