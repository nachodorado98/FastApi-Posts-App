import pytest

def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()[0]=="bbdd_posts"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla[0] for tabla in conexion.c.fetchall()]

	assert "posts" in tablas


def test_tabla_vacia(conexion):

	conexion.c.execute("SELECT * FROM posts")

	assert conexion.c.fetchall()==[]


def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed


