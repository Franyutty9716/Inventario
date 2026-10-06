from fastapi import FastAPI
from db import crear_tablas, listar_productos

app = FastAPI()

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