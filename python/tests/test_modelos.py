import datetime

from src.modelos.modelos_post import Post
from src.modelos.utils_modelos import obtener_objeto_post, obtener_objetos_post

def test_obtener_objeto_post():

	post={"id":1, "titulo":"Titulo", "contenido":"Contenido", "fecha":datetime.datetime(2023,8,3)}

	objeto_post=obtener_objeto_post(post)

	assert isinstance(objeto_post, Post)
	assert objeto_post.id==1
	assert objeto_post.titulo=="Titulo"
	assert objeto_post.contenido=="Contenido"
	assert objeto_post.fecha=="03/08/2023"

def test_obtener_objetos_post():

	posts=[{"id":1, "titulo":"Titulo", "contenido":"Contenido", "fecha":datetime.datetime(2023,8,3)},
			{"id":2, "titulo":"Titulo2", "contenido":"Contenido2", "fecha":datetime.datetime(2023,8,4)},
			{"id":3, "titulo":"Titulo3", "contenido":"Contenido3", "fecha":datetime.datetime(2023,8,5)}]

	objetos_post=obtener_objetos_post(posts)

	assert len(objetos_post)==3

	for objeto in objetos_post:

		assert isinstance(objeto, Post)