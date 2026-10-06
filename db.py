import sqlite3

#Abre la conexion con la base de datos (la crea si no existe)
def conectar():
    return sqlite3.connect("inventario.db")

#Crea las tablas si todavia no existen
def crear_tablas():
    conexion = conectar()
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 0,
            precio REAL NOT NULL,
            minimo INTEGER NOT NULL DEFAULT 5
        )
    """)
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conexion.commit()
    conexion.close()

#Agrega un producto nuevo a la tabla 
def agregar_producto(nombre, cantidad, precio, minimo):
    conexion = conectar()
    conexion.execute(
        "INSERT INTO productos (nombre, cantidad, precio, minimo) VALUES (?, ?, ?, ?)",
        (nombre, cantidad, precio, minimo)
    )
    conexion.commit()
    conexion.close()

#Devuelve todos los productos como una lista
def listar_productos():
    conexion = conectar()
    filas = conexion.execute(
        "SELECT id, nombre, cantidad, precio, minimo FROM productos ORDER BY nombre"
    ).fetchall()
    conexion.close()
    return filas

#Busca productos cuyo nombre contenga el texto indicado
def buscar_productos(texto):
    conexion = conectar()
    filas = conexion.execute(
        "SELECT id, nombre, cantidad, precio, minimo FROM productos WHERE nombre LIKE ? ORDER BY nombre",
        ("%" + texto + "%",)
    ).fetchall()
    conexion.close()
    return filas

#Registra una entrada o salida y actualiza la cantidad del producto
def registrar_movimiento(producto_id, tipo, cantidad):
    conexion = conectar()
    fila = conexion.execute(
        "SELECT cantidad FROM productos WHERE id = ?",
        (producto_id,)
    ).fetchone()
    if fila is None:
        conexion.close()
        return "El producto no existe."
    stock = fila[0]
    if tipo == "salida" and cantidad > stock:
        conexion.close()
        return "No hay suficiente stock."
    if tipo == "entrada":
        nuevo_stock = stock + cantidad
    else:
        nuevo_stock = stock - cantidad
    conexion.execute(
        "UPDATE productos SET cantidad = ? WHERE id = ?",
        (nuevo_stock, producto_id)
    )
    conexion.execute(
        "INSERT INTO movimientos (producto_id, tipo, cantidad) VALUES (?, ?, ?)",
        (producto_id, tipo, cantidad)
    )
    conexion.commit()
    conexion.close()
    return "Movimiento registrado."

#Devuelve los productos cuya cantidad es igual o menor a su minimo
def productos_stock_bajo():
    conexion = conectar()
    filas = conexion.execute(
        "SELECT id, nombre, cantidad, precio, minimo FROM productos WHERE cantidad <= minimo ORDER BY cantidad"
    ).fetchall()
    conexion.close()
    return filas