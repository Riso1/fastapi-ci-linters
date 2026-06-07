from wsgiref.simple_server import make_server

from routes import app


if __name__ == "__main__":
    server = make_server("127.0.0.1", 8000, app)
    print("Сервер запущен на http://127.0.0.1:8000")
    server.serve_forever()
