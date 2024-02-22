# run.py
from app.app import app, socketio  # Import both app and socketio

if __name__ == "__main__":
    socketio.run(app, debug=True)  # Use socketio.run instead of app.run
