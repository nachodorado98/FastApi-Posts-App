import pytest

def test_pagina_obtener_posts_vacio(cliente, conexion):

	respuesta=cliente.get("/posts")

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert contenido==[]


def test_agregar_post_ok(cliente, conexion):

	post={"titulo":"Titulo del post", "contenido":"Contenido del post"}

	respuesta=cliente.post("/posts", json=post)

	contenido=respuesta.json()

	assert respuesta.status_code==201
	assert "mensaje" in contenido
	assert "post" in contenido
	assert contenido["post"]==post

	posts=conexion.obtenerPosts()

	assert posts[0]["titulo"]=="Titulo del post"
	assert posts[0]["contenido"]=="Contenido del post"


@pytest.mark.parametrize(["post"],
	[
		({"titulo":"Titulo del post", "contenido":13},),
		({"titulo":22, "contenido":"Contenido del post"},),
		({"titulo":"Titulo del post"},),
		({"contenido":"Contenido del post"},),
		({},),
		({"Titulo":"Titulo del post", "Contenido":"Contenido del post"},),
	]
)
def test_agregar_post_incorrecto(cliente, conexion, post):

	respuesta=cliente.post("/posts", json=post)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "post" in contenido

	posts=conexion.obtenerPosts()

	assert posts==[]

def test_obtener_posts(cliente, conexion):

	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})

	respuesta=cliente.get("/posts")

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert contenido[0]["titulo"]=="Titulo del post"
	assert contenido[0]["contenido"]=="Contenido del post"
