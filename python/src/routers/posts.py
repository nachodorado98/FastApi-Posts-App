from fastapi import APIRouter, status
from typing import Dict

from src.database.conexion import Conexion


router_posts=APIRouter(prefix="/posts", tags=["Posts"])


@router_posts.get("", status_code=status.HTTP_200_OK, summary="Devuelve los posts existentes")
async def obtenerPosts()->Dict:

	"""

	Devuelve los diccionarios que representan los posts disponibles.

    ## Respuesta

    200 (OK): Si se obtienen los posts correctamente

    - **Id**: El ID del post (int).
    - **Titulo**: El titulo del post (str).
    - **Contenido**: El contenido del post (str).
    - **Fecha**: La fecha del post (str).
    """
    
	con=Conexion()

	con.c.execute("SELECT * FROM posts")

	posts=con.c.fetchall()

	con.cerrarConexion()

	return {"posts":posts}