# wsgi.py - entry point for gunicorn and local run

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Optional: allows local run with `python wsgi.py`
    app.run(host="0.0.0.0", port=5000, debug=True)