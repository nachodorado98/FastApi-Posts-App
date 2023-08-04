import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, List

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:
			
			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")
			print(e)

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para obtener todos los posts
	def obtenerPosts(self)->List[Dict]:

		self.c.execute("""SELECT *
						FROM posts""")

		return self.c.fetchall()

	# Metodo para insertar un post
	def insertarPost(self, titulo:str, contenido:str, fecha:str)->None:

		self.c.execute("""INSERT INTO posts (titulo, contenido, fecha)
						VALUES(%s, %s, %s)""",
						(titulo, contenido, fecha))

		self.bbdd.commit()

	# Metodo para obtener un post por su id
	def obtenerPost(self, identificador:int)->Optional[Dict]:

		self.c.execute("""SELECT *
						FROM posts
						WHERE id=%s""",
						(identificador,))

		return self.c.fetchone()

	# Metodo para actualizar un post por su id
	def actualizarPost(self, identificador:int, titulo:str, contenido:str)->None:

		self.c.execute("""UPDATE posts
						SET titulo=%s, contenido=%s
						WHERE id=%s""",
						(titulo, contenido, identificador))

		self.bbdd.commit()

	# Metodo para eliminar todos los posts
	def eliminarPosts(self)->None:

		self.c.execute("""DELETE FROM posts""")

		self.bbdd.commit()

	# Metodo para eliminar un post por su id
	def eliminarPost(self, identificador:int)->None:

		self.c.execute("""DELETE FROM posts
						WHERE id=%s""",
						(identificador,))

		self.bbdd.commit()



