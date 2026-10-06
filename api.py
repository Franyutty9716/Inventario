from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import crear_tablas, listar_productos, agregar_producto, productos_stock_bajo, registrar_movimiento

app = FastAPI()

#Define los datos que debe traer un producto (FastAPI los valida solo)
class Producto(BaseModel):
    nombre: str
    cantidad: int
    precio: float
    minimo: int

#Define los datos de un movimiento de inventario
class Movimiento(BaseModel):
    producto_id: int
    tipo: str
    cantidad: int

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

#Devuelve los productos que estan por acabarse
@app.get("/stock-bajo")
def ver_stock_bajo():
    productos = []
    for id, nombre, cantidad, precio, minimo in productos_stock_bajo():
        productos.append({
            "id": id,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
            "minimo": minimo
        })
    return productos

#Registra una entrada o salida de mercancia
@app.post("/movimientos")
def crear_movimiento(movimiento: Movimiento):
    if movimiento.tipo not in ("entrada", "salida"):
        raise HTTPException(status_code=400, detail="El tipo debe ser entrada o salida.")
    if movimiento.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a cero.")
    mensaje = registrar_movimiento(movimiento.producto_id, movimiento.tipo, movimiento.cantidad)
    if mensaje != "Movimiento registrado.":
        raise HTTPException(status_code=400, detail=mensaje)
    return {"mensaje": mensaje}