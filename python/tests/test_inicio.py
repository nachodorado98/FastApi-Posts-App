def test_pagina_inicio(cliente):

	contenido=cliente.get("/").json()

	assert contenido=={"Bienvenido":"Hola Mundo"}
