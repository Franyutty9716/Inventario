import sqlite3

#Abre la conexion con la base de datos (la crea si no existe)
def conectar():
    return sqlite3.connect("inventario.db")

#Crea la tabla de productos si todavia no existe
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