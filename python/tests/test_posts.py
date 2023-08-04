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


@pytest.mark.parametrize(["id_incorrecto"],
	[("uno",),("hola",), ("dos",)]
)
def test_obtener_post_incorrecto(cliente, conexion, id_incorrecto):

	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})

	respuesta=cliente.get(f"/posts/{id_incorrecto}")

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "titulo" in contenido
	assert not "contenido" in contenido


@pytest.mark.parametrize(["id_no_existe"],
	[("0",),("1",), ("-1",)]
)
def test_obtener_post_no_existente(cliente, conexion, id_no_existe):

	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})

	respuesta=cliente.get(f"/posts/{id_no_existe}")

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido


def test_obtener_post_existente(cliente, conexion):

	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})

	respuesta=cliente.get("/posts")

	post=respuesta.json()[0]

	id_post=post["id"]

	respuesta_buscado=cliente.get(f"/posts/{id_post}")

	contenido=respuesta_buscado.json()

	assert respuesta_buscado.status_code==200
	assert contenido["titulo"]=="Titulo del post"
	assert contenido["contenido"]=="Contenido del post"


@pytest.mark.parametrize(["id_incorrecto", "post"],
	[
		("uno", {"titulo":"Titulo nuevo del post", "contenido":"Contenido nuevo del post"}),
		("hola", {"titulo":"Titulo nuevo del post", "contenido":"Contenido nuevo del post"}),
		("dos", {"titulo":"Titulo nuevo del post", "contenido":"Contenido nuevo del post"}),
		("1", {"titulo":"Titulo nuevo del post", "contenido":1}),
		("22", {"titulo":"Titulo nuevo del post"}),
		("6", {"contenido":"Contenido nuevo del post"}),
		("13", {}),
	]
)
def test_actualizar_post_incorrecto(cliente, conexion, id_incorrecto, post):

	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})

	respuesta=cliente.put(f"/posts/{id_incorrecto}", json=post)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "post" in contenido


@pytest.mark.parametrize(["id_no_existe"],
	[("0",),("1",), ("-1",)]
)
def test_actualizar_post_no_existente(cliente, conexion, id_no_existe):

	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})

	respuesta=cliente.put(f"/posts/{id_no_existe}", json={"titulo":"Titulo nuevo del post", "contenido":"Contenido nuevo del post"})

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido


def test_actualizar_post_existente(cliente, conexion):

	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})

	respuesta=cliente.get("/posts")

	post=respuesta.json()[0]

	id_post=post["id"]

	cliente.put(f"/posts/{id_post}", json={"titulo":"Titulo nuevo", "contenido":"Contenido nuevo del post"})

	respuesta_actualizado=cliente.get(f"/posts/{id_post}")

	contenido=respuesta_actualizado.json()

	assert respuesta_actualizado.status_code==200
	assert contenido["titulo"]=="Titulo nuevo"
	assert contenido["contenido"]=="Contenido nuevo del post"


def test_eliminar_posts_existentes(cliente, conexion):

	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})
	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})
	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})

	respuesta=cliente.get("/posts")

	assert len(respuesta.json())==3

	respuesta_eliminar=cliente.delete("/posts")

	contenido=respuesta_eliminar.json()

	assert respuesta_eliminar.status_code==200
	assert "mensaje" in contenido

	respuesta_verificar=cliente.get("/posts")

	assert len(respuesta_verificar.json())==0







@pytest.mark.parametrize(["id_incorrecto"],
	[("uno",),("hola",), ("dos",)]
)
def test_eliminar_post_incorrecto(cliente, conexion, id_incorrecto):

	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})

	respuesta=cliente.delete(f"/posts/{id_incorrecto}")

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido


@pytest.mark.parametrize(["id_no_existe"],
	[("0",),("1",), ("-1",)]
)
def test_eliminar_post_no_existente(cliente, conexion, id_no_existe):

	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})

	respuesta=cliente.delete(f"/posts/{id_no_existe}")

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido


def test_eliminar_post_existente(cliente, conexion):

	cliente.post("/posts", json={"titulo":"Titulo del post", "contenido":"Contenido del post"})

	respuesta=cliente.get("/posts")

	post=respuesta.json()[0]

	id_post=post["id"]

	respuesta_eliminado=cliente.delete(f"/posts/{id_post}")

	contenido=respuesta_eliminado.json()

	assert respuesta_eliminado.status_code==200
	assert "mensaje" in contenido

	respuesta_verificar=cliente.get("/posts")

	assert len(respuesta_verificar.json())==0

