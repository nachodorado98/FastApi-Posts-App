def test_pagina_leer_posts(cliente):

	respuesta=cliente.get("/posts")

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert contenido=={"posts":[]}
