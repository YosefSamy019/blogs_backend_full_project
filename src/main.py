from fastapi import FastAPI
import uvicorn

from src.shared.sl import Sl
from src.app.routes.routes_init import routes_init

app = FastAPI()


def main():
    global app
    # Init Sl
    Sl()

    # Init routes
    routes_init(app=app)


main()

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
