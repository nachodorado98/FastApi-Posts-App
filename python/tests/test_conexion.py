import pytest
import datetime

def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_posts"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "posts" in tablas


def test_tabla_vacia(conexion):

	conexion.c.execute("SELECT * FROM posts")

	assert conexion.c.fetchall()==[]


def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed


@pytest.mark.parametrize(["titulo", "contenido", "anno", "mes", "dia"],
	[
		("Mi post", "Contenido", "2023", "08", "03"),
		("Mi post2", "Me gustan los buses", "2019", "06", "22"),
		("Titulo post", "fdhgfjgfj", "2029", "04", "13")
	]
)
def test_obtener_posts(conexion, titulo, contenido, anno, mes, dia):

	conexion.c.execute("INSERT INTO posts (titulo, contenido, fecha) VALUES (%s, %s, %s)",
						(titulo, contenido, f"{anno}-{mes}-{dia}"))

	conexion.bbdd.commit()

	posts=conexion.obtenerPosts()

	assert posts[0]["titulo"]==titulo
	assert posts[0]["contenido"]==contenido
	assert posts[0]["fecha"]==datetime.date(int(anno), int(mes), int(dia))


def test_insertar_post(conexion):

	conexion.insertarPost("Titulo", "Contenido", "2023-08-03")

	posts=conexion.obtenerPosts()

	assert posts[0]["titulo"]=="Titulo"
	assert posts[0]["contenido"]=="Contenido"
	assert posts[0]["fecha"]==datetime.date(2023, 8, 3)


def test_insertar_multiples_posts(conexion):

	conexion.insertarPost("Titulo", "Contenido", "2023-08-03")
	conexion.insertarPost("Titulo2", "Contenido1", "2023-08-04")
	conexion.insertarPost("Titulo3", "Contenido2", "2023-08-05")

	posts=conexion.obtenerPosts()

	assert len(posts)==3


def test_obtener_post_id_existe(conexion):

	conexion.insertarPost("Titulo", "Contenido", "2023-08-03")

	post=conexion.obtenerPosts()[0]

	id_post=post["id"]

	post_buscado=conexion.obtenerPost(id_post)

	assert post_buscado["id"]==id_post
	assert post_buscado["titulo"]=="Titulo"
	assert post_buscado["contenido"]=="Contenido"
	assert post_buscado["fecha"]==datetime.date(2023, 8, 3)


def test_obtener_post_id_no_existe(conexion):

	assert conexion.obtenerPost(1) is None


def test_actualizar_post_id(conexion):

	conexion.insertarPost("Titulo", "Contenido", "2023-08-03")

	post=conexion.obtenerPosts()[0]

	id_post=post["id"]

	conexion.actualizarPost(id_post, "Nuevo Titulo", "Nuevo Contenido")

	post_actualizado=conexion.obtenerPost(id_post)

	assert post_actualizado["id"]==id_post
	assert post_actualizado["titulo"]=="Nuevo Titulo"
	assert post_actualizado["contenido"]=="Nuevo Contenido"
	assert post_actualizado["fecha"]==datetime.date(2023, 8, 3)


def test_eliminar_posts(conexion):

	conexion.insertarPost("Titulo", "Contenido", "2023-08-03")
	conexion.insertarPost("Titulo2", "Contenido1", "2023-08-04")
	conexion.insertarPost("Titulo3", "Contenido2", "2023-08-05")

	assert len(conexion.obtenerPosts())==3

	conexion.eliminarPosts()

	assert len(conexion.obtenerPosts())==0


def test_eliminar_post_id(conexion):

	conexion.insertarPost("Titulo", "Contenido", "2023-08-03")

	post=conexion.obtenerPosts()[0]

	id_post=post["id"]

	assert not conexion.obtenerPost(id_post) is None

	conexion.eliminarPost(id_post)

	assert conexion.obtenerPost(id_post) is None


def test_obtener_ultimo_post_existe(conexion):

	conexion.insertarPost("Titulo", "Contenido", "2023-08-03")
	conexion.insertarPost("Titulo", "Contenido", "2023-08-03")
	conexion.insertarPost("Titulo", "Contenido", "2023-08-03")
	conexion.insertarPost("Titulo ultimo", "Contenido ultimo", "2023-08-05")

	ultimo_post=conexion.obtenerUltimo()

	assert ultimo_post["titulo"]=="Titulo ultimo"
	assert ultimo_post["contenido"]=="Contenido ultimo"
	assert ultimo_post["fecha"]==datetime.date(2023, 8, 5)


def test_obtener_ultimo_post_no_existe(conexion):

	assert conexion.obtenerUltimo() is None


def test_obtener_primer_post_existe(conexion):

	conexion.insertarPost("Titulo primero", "Contenido primero", "2023-08-03")
	conexion.insertarPost("Titulo", "Contenido", "2023-08-05")
	conexion.insertarPost("Titulo", "Contenido", "2023-08-05")
	conexion.insertarPost("Titulo", "Contenido", "2023-08-05")

	primer_post=conexion.obtenerPrimero()

	assert primer_post["titulo"]=="Titulo primero"
	assert primer_post["contenido"]=="Contenido primero"
	assert primer_post["fecha"]==datetime.date(2023, 8, 3)


def test_obtener_primer_post_no_existe(conexion):

	assert conexion.obtenerPrimero() is None















