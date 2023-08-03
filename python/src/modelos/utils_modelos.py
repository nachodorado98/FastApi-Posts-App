from typing import Dict, List

from .modelos_post import Post

# Funcion para obtener un objeto Post
def obtener_objeto_post(valores:Dict)->Post:

	return Post(id=valores["id"],
				titulo=valores["titulo"],
				contenido=valores["contenido"],
				fecha=valores["fecha"].strftime("%d/%m/%Y"))


# Funcion para obtener una lista de objetos Post
def obtener_objetos_post(posts:List[Dict])->List[Post]:

	return [obtener_objeto_post(post) for post in posts]

