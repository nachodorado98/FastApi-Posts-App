import os
import sys
sys.path.append("..")

import pytest
from src import crear_app
from fastapi.testclient import TestClient 

@pytest.fixture()
def app():

	app=crear_app()

	return app


@pytest.fixture()
def cliente(app):

	return TestClient(app)

