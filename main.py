from db import crear_tablas, agregar_producto, listar_productos

#Muestra las opciones del menu
def mostrar_menu():
    print("=== Menu de Inventario ===")
    print("1. Agregar producto")
    print("2. Listar productos")
    print("3. Salir")

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
crear_tablas()

while True:
    mostrar_menu()
    opcion = input("Elige una opcion: ")
    if opcion == "1":
        pedir_producto()
    elif opcion == "2":
        mostrar_productos()
    elif opcion == "3":
        print("Hasta luego")
        break
    else:
        print("Opcion no valida.")