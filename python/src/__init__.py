from fastapi import FastAPI

from .routers.inicio import router_inicio

# Funcion para crear la app
def crear_app():

	app=FastAPI()

	app.include_router(router_inicio)

	return app