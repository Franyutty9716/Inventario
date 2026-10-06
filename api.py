from fastapi import FastAPI
from pydantic import BaseModel
from db import crear_tablas, listar_productos, agregar_producto

app = FastAPI()

#Define los datos que debe traer un producto (FastAPI los valida solo)
class Producto(BaseModel):
    nombre: str
    cantidad: int
    precio: float
    minimo: int

#Al encender la API, me aseguro de que las tablas existan
crear_tablas()

#Ruta de prueba: responde en la direccion principal
@app.get("/")
def inicio():
    return {"mensaje": "API del inventario funcionando"}

#Devuelve todos los productos
@app.get("/productos")
def ver_productos():
    productos = []
    for id, nombre, cantidad, precio, minimo in listar_productos():
        productos.append({
            "id": id,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
            "minimo": minimo
        })
    return productos

#Recibe un producto nuevo y lo guarda en la base de datos
@app.post("/productos")
def crear_producto(producto: Producto):
    agregar_producto(producto.nombre, producto.cantidad, producto.precio, producto.minimo)
    return {"mensaje": "Producto agregado"}