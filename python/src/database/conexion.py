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


# Funcion para devolver el objeto de la conexion
def obtenerConexion()->Optional[Conexion]:

	con=Conexion()

	try: 

		yield con

	except:

		con.cerrarConexion()

