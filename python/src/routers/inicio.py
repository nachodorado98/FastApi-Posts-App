from fastapi import APIRouter
from typing import Dict


router_inicio=APIRouter()


@router_inicio.get("/")
async def inicio()->Dict:

	return {"Bienvenido":"Hola Mundo"}