from src.app.routes.routes_init import routes_init

from fastapi import FastAPI

from src.shared.sl import Sl

app = FastAPI()



def main():
    global app
    # Init Sl
    Sl()

    # Init routes
    routes_init(app=app)


main()
