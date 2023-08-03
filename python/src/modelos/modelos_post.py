from pydantic import BaseModel

# Clase para un post basico
class PostBasico(BaseModel):

	titulo:str
	contenido:str

# Clase para un post completo
class Post(PostBasico):

	id:int
	fecha:str