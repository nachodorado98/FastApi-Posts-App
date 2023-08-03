from fastapi import APIRouter, status, Depends
from typing import List, Dict
import datetime

from src.database.conexion import Conexion, obtenerConexion
from src.modelos.modelos_post import Post, PostBasico
from src.modelos.utils_modelos import obtener_objetos_post


router_posts=APIRouter(prefix="/posts", tags=["Posts"])


@router_posts.get("", status_code=status.HTTP_200_OK, summary="Devuelve los posts existentes")
async def obtenerPosts(con:Conexion=Depends(obtenerConexion))->List[Post]:

	"""
	Devuelve los diccionarios que representan los posts disponibles.

	## Respuesta

	200 (OK): Si se obtienen los posts correctamente

	- **Id**: El ID del post (int).
	- **Titulo**: El titulo del post (str).
	- **Contenido**: El contenido del post (str).
	- **Fecha**: La fecha del post (str).
	"""

	posts=con.obtenerPosts()

	objetos_post=obtener_objetos_post(posts)

	con.cerrarConexion()

	return objetos_post


@router_posts.post("", status_code=status.HTTP_201_CREATED, summary="Creacion de un post")
async def agregarPost(post:PostBasico, con:Conexion=Depends(obtenerConexion))->Dict:

	"""
	Crea un post y lo inserta en la base de datos. Devuelve un mensaje y el diccionario que representa el post creado.

	## Respuesta

	201 (CREADO): Si se crea el post correctamente

	- **Mensaje**: El mensaje de creacion correcto del post (str).
	- **Post**: El post con el titulo y el contenido (Dict).
	"""

	fecha_actual=datetime.datetime.now().strftime("%Y-%m-%d")

	con.insertarPost(post.titulo, post.contenido, fecha_actual)

	con.cerrarConexion()

	return {"mensaje":"Post creado con exito",
			"post":post}