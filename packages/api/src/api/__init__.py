from apiflask import APIFlask
app = APIFlask("greenhouse_dt_api")

def main() -> None:
    app.run()