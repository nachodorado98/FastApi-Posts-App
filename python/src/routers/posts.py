from fastapi import APIRouter, status, Depends, Path, HTTPException
from typing import List, Dict
import datetime

from src.database.sesion import Conexion, crearConexion
from src.modelos.modelos_post import Post, PostBasico
from src.modelos.utils_modelos import obtener_objetos_post, obtener_objeto_post


router_posts=APIRouter(prefix="/posts", tags=["Posts"])


@router_posts.get("", status_code=status.HTTP_200_OK, summary="Devuelve los posts existentes")
async def obtenerPosts(con:Conexion=Depends(crearConexion))->List[Post]:

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
async def agregarPost(post:PostBasico, con:Conexion=Depends(crearConexion))->Dict:

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


@router_posts.get("/ultimo", status_code=status.HTTP_200_OK, summary="Devuelve el ultimo post")
async def obtenerUltimo(con:Conexion=Depends(crearConexion))->Post:

	"""
	Devuelve el diccionario del ultimo post.

	## Respuesta

	200 (OK): Si se obtiene el ultimo post correctamente

	- **Id**: El ID del post (int).
	- **Titulo**: El titulo del post (str).
	- **Contenido**: El contenido del post (str).
	- **Fecha**: La fecha del post (str).

	404 (NOT FOUND): Si no se obtiene el ultimo post correctamente

	- **Detail**: El mensaje del detalle de la excepcion (str).

	"""

	post=con.obtenerUltimo()

	if post is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no existente")

	objeto_post=obtener_objeto_post(post)

	con.cerrarConexion()

	return objeto_post


@router_posts.get("/primero", status_code=status.HTTP_200_OK, summary="Devuelve el primer post")
async def obtenerPrimero(con:Conexion=Depends(crearConexion))->Post:

	"""
	Devuelve el diccionario del primer post.

	## Respuesta

	200 (OK): Si se obtiene el primer post correctamente

	- **Id**: El ID del post (int).
	- **Titulo**: El titulo del post (str).
	- **Contenido**: El contenido del post (str).
	- **Fecha**: La fecha del post (str).

	404 (NOT FOUND): Si no se obtiene el primer post correctamente

	- **Detail**: El mensaje del detalle de la excepcion (str).

	"""

	post=con.obtenerPrimero()

	if post is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no existente")

	objeto_post=obtener_objeto_post(post)

	con.cerrarConexion()

	return objeto_post


@router_posts.get("/{id_post}", status_code=status.HTTP_200_OK, summary="Devuelve el post buscado")
async def obtenerPost(id_post:int=Path(..., title="Id del post", description="Id unico del post que quieres obtener"),
						con:Conexion=Depends(crearConexion))->Post:

	"""
	Devuelve el diccionario del post buscado a traves de su id.

	## Parametros

	- **Id_post**: El ID del post (int).

	## Respuesta

	200 (OK): Si se obtiene el post correctamente

	- **Id**: El ID del post (int).
	- **Titulo**: El titulo del post (str).
	- **Contenido**: El contenido del post (str).
	- **Fecha**: La fecha del post (str).

	404 (NOT FOUND): Si no se obtiene el post correctamente

	- **Detail**: El mensaje del detalle de la excepcion (str).

	"""

	post=con.obtenerPost(id_post)

	if post is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no existente")

	objeto_post=obtener_objeto_post(post)

	con.cerrarConexion()

	return objeto_post


@router_posts.put("/{id_post}", status_code=status.HTTP_200_OK, summary="Actualiza el post indicado")
async def actualizarPost(post:PostBasico,
						id_post:int=Path(..., title="Id del post", description="Id unico del post que quieres actualizar"),
						con:Conexion=Depends(crearConexion))->Dict:

	"""
	Actualiza el diccionario del post buscado a traves de su id.

	## Parametros

	- **Id_post**: El ID del post (int).

	## Respuesta

	200 (OK): Si se actualiza el post correctamente

	- **Mensaje**: El mensaje de actualizacion correcto del post (str).
	- **Post**: El post con el titulo y el contenido (Dict).

	404 (NOT FOUND): Si no se actualiza el post correctamente

	- **Detail**: El mensaje del detalle de la excepcion (str).

	"""

	if con.obtenerPost(id_post) is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no existente")

	con.actualizarPost(id_post, post.titulo, post.contenido)

	con.cerrarConexion()

	return {"mensaje":"Post actualizado con exito",
			"post":post}


@router_posts.delete("", status_code=status.HTTP_200_OK, summary="Elimina todos los posts existentes")
async def eliminarPosts(con:Conexion=Depends(crearConexion))->Dict:

	"""
	Elimina los diccionarios que representan los posts disponibles.

	## Respuesta

	200 (OK): Si se eliminan los posts correctamente

	-  **Mensaje**: El mensaje de eliminacion correcto de los posts (str).
	"""

	con.eliminarPosts()

	con.cerrarConexion()

	return {"mensaje":"Posts eliminados con exito"}


@router_posts.delete("/{id_post}", status_code=status.HTTP_200_OK, summary="Elimina el post indicado")
async def eliminarPost(id_post:int=Path(..., title="Id del post", description="Id unico del post que quieres actualizar"),
						con:Conexion=Depends(crearConexion))->Dict:

	"""
	Elimina el diccionario del post buscado a traves de su id.

	## Parametros

	- **Id_post**: El ID del post (int).

	## Respuesta

	200 (OK): Si se elimina el post correctamente

	-  **Mensaje**: El mensaje de eliminacion correcto del post (str).

	404 (NOT FOUND): Si no se elimina el post correctamente

	- **Detail**: El mensaje del detalle de la excepcion (str).

	"""

	if con.obtenerPost(id_post) is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no existente")

	con.eliminarPost(id_post)

	con.cerrarConexion()

	return {"mensaje":"Post eliminado con exito"}



