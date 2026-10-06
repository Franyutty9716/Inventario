from db import crear_tablas, agregar_producto, listar_productos, buscar_productos, registrar_movimiento

#Muestra las opciones del menu
def mostrar_menu():
    print("=== Menu de Inventario ===")
    print("1. Agregar producto")
    print("2. Listar productos")
    print("3. Buscar producto")
    print("4. Registrar entrada")
    print("5. Registrar salida")
    print("6. Salir")

#Pide los datos de un prducto y lo guarda 
def pedir_producto():
    nombre = input("Nombre:")
    try:
        cantidad = int(input("Cantidad:"))
        precio = float(input("Precio:"))
        minimo = int(input("Cantidad Minima:"))
    except ValueError:
        print("Cantidad y mninimo deben ser enteros y el precio un numero.")
        return
    agregar_producto(nombre, cantidad, precio, minimo)
    print("Producto agregado.")

#Muestra todos los productos guardados
def mostrar_productos():
    productos = listar_productos()
    if len(productos) == 0:
        print("Aun no hay productos.")
        return
    for id, nombre, cantidad, precio, minimo in productos:
        print(f"{id}. {nombre} - {cantidad} piezas - ${precio}")

#Pide un texto y muestra los productos que coincidan
def mostrar_busqueda():
    texto = input("Buscar producto: ")
    productos = buscar_productos(texto)
    if len(productos) == 0:
        print("No se encontraron productos.")
        return
    for id, nombre, cantidad, precio, minimo in productos:
        print(f"{id}. {nombre} - {cantidad} piezas - ${precio}")

#Pide los datos de un movimiento y lo registra
def pedir_movimiento(tipo):
    mostrar_productos()
    try:
        producto_id = int(input("Numero del producto: "))
        cantidad = int(input("Cantidad: "))
    except ValueError:
        print("Escribe solo numeros enteros.")
        return
    if cantidad <= 0:
        print("La cantidad debe ser mayor a cero.")
        return
    mensaje = registrar_movimiento(producto_id, tipo, cantidad)
    print(mensaje)

crear_tablas()

while True:
    mostrar_menu()
    opcion = input("Elige una opcion: ")
    if opcion == "1":
        pedir_producto()
    elif opcion == "2":
        mostrar_productos()
    elif opcion == "3":
        mostrar_busqueda()
    elif opcion == "4":
        pedir_movimiento("entrada")
    elif opcion == "5":
        pedir_movimiento("salida")
    elif opcion == "6":
        print("Hasta luego")
        break
    else:
        print("Opcion no valida.")