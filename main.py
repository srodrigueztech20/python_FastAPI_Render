from fastapi import FastAPI , HTTPException
from typing import Optional
from pydantic import BaseModel
import uuid  # generador del id 



app = FastAPI()

# ------ Defino el Modelo -----

class Curso(BaseModel):
    id: Optional[str] = None
    descripcion: Optional[str] = None
    nombre: str
    nivel: str
    duracion: int
    
# Simulo una base de datos

cursos_db = []

# CRUD: Read (lectura) GET ALL : Leemos todos los cursos de la db

@app.get("/cursos/", response_model=list[Curso])
def obtener_cursos():
    return cursos_db

# CRUD: Create (escribir) POST: agrego un nuevo recurso

@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) # UUID4 - me da un 'id' unico e irrepetible
    cursos_db.append(curso)
    return curso

# CRUD: Read (leer) GET : individual 

@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException (status_code=404, detail="Curso no encontrado")
    return curso


# CRUD: Update (Actualizar/Modificar) PUT - individual

@app.put ("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException (status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso)
    cursos_db[index] = curso_actualizado
    return curso_actualizado

# CRUD: Delete (Borrado/Baja) DELETE

@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException (status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso
 
