from main import app, init_logging

if __name__ == "__main__":
    init_logging()
    app.run(debug=False)