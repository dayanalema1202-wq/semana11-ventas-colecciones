from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante

OPCIONES_MENU: tuple[tuple[str, str], ...] = (
    ("1",  "Registrar producto"),
    ("2",  "Buscar producto"),
    ("3",  "Actualizar producto"),
    ("4",  "Eliminar producto"),
    ("5",  "Listar productos"),
    ("6",  "Registrar usuario"),
    ("7",  "Buscar usuario"),
    ("8",  "Actualizar usuario"),
    ("9",  "Eliminar usuario"),
    ("10", "Listar usuarios"),
    ("11", "Realizar venta"),
    ("12", "Consultar ventas de un usuario"),
    ("13", "Listar todas las ventas"),
    ("14", "Categorias disponibles"),
    ("0",  "Salir"),
)


def pedir_texto(mensaje: str) -> str:
    return input(mensaje).strip()


def pedir_entero(mensaje: str) -> int:
    return int(pedir_texto(mensaje))


def pedir_decimal(mensaje: str) -> float:
    return float(pedir_texto(mensaje))


def pedir_booleano(mensaje: str) -> bool:
    respuesta = pedir_texto(mensaje + " (s/n): ").lower()
    return respuesta == "s"


def mostrar_menu() -> None:
    print("\n~~~ RESTAURANTE APP ~~~")
    print("\nPRODUCTOS:")
    for opcion, descripcion in OPCIONES_MENU[:5]:
        print(f"  [{opcion}] {descripcion}")
    print("\nUSUARIOS:")
    for opcion, descripcion in OPCIONES_MENU[5:10]:
        print(f"  [{opcion}] {descripcion}")
    print("\nVENTAS:")
    for opcion, descripcion in OPCIONES_MENU[10:13]:
        print(f"  [{opcion}] {descripcion}")
    print("\nCONSULTAS:")
    print(f"  [{OPCIONES_MENU[13][0]}] {OPCIONES_MENU[13][1]}")
    print("\n  [0] Salir")


def guardar_productos(archivo: ArchivoServicio, restaurante: Restaurante) -> None:
    if not archivo.guardar_productos(restaurante.listar_productos()):
        print("No fue posible guardar los productos.")


def guardar_usuarios(archivo: ArchivoServicio, restaurante: Restaurante) -> None:
    if not archivo.guardar_usuarios(restaurante.listar_usuarios()):
        print("No fue posible guardar los usuarios.")


def guardar_ventas(archivo: ArchivoServicio, restaurante: Restaurante) -> None:
    if not archivo.guardar_ventas(restaurante.listar_ventas()):
        print("No fue posible guardar las ventas.")


def registrar_producto(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Registrar producto ---")
    print(f"Categorias disponibles: {', '.join(Producto.CATEGORIAS_VALIDAS)}")
    codigo = pedir_texto("Codigo: ")
    nombre = pedir_texto("Nombre del plato: ")
    try:
        precio = pedir_decimal("Precio ($): ")
        categoria = pedir_texto("Categoria: ")
        es_vegetariano = pedir_booleano("Es vegetariano")
        stock = pedir_entero("Stock inicial: ")
        producto = Producto(codigo, nombre, precio, categoria, es_vegetariano, stock)
        if restaurante.registrar_producto(producto):
            print("Plato registrado en el menu.")
            guardar_productos(archivo, restaurante)
        else:
            print("Ya existe un producto con ese codigo.")
    except ValueError as error:
        print(f"Dato invalido: {error}")


def buscar_producto(restaurante: Restaurante) -> None:
    print("\n--- Buscar producto ---")
    codigo = pedir_texto("Codigo del plato: ")
    resultado = restaurante.buscar_producto(codigo)
    print(resultado if resultado else "Plato no encontrado.")


def actualizar_producto(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Actualizar producto ---")
    codigo = pedir_texto("Codigo a actualizar: ")
    if restaurante.buscar_producto(codigo) is None:
        print("Producto no encontrado.")
        return
    print(f"Categorias: {', '.join(Producto.CATEGORIAS_VALIDAS)}")
    try:
        nuevo_nombre = pedir_texto("Nuevo nombre: ")
        nuevo_precio = pedir_decimal("Nuevo precio: ")
        nueva_categoria = pedir_texto("Nueva categoria: ")
        nuevo_vegetariano = pedir_booleano("Es vegetariano")
        nuevo_stock = pedir_entero("Nuevo stock: ")
        if restaurante.actualizar_producto(codigo, nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_vegetariano, nuevo_stock):
            print("Producto actualizado.")
            guardar_productos(archivo, restaurante)
        else:
            print("No se pudo actualizar.")
    except ValueError as error:
        print(f"Dato invalido: {error}")


def eliminar_producto(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Eliminar producto ---")
    codigo = pedir_texto("Codigo: ")
    if restaurante.eliminar_producto(codigo):
        print("Producto eliminado del menu.")
        guardar_productos(archivo, restaurante)
    else:
        print("Producto no encontrado.")


def listar_productos(restaurante: Restaurante) -> None:
    print("\n--- Menu del restaurante ---")
    productos = restaurante.listar_productos()
    if not productos:
        print("El menu esta vacio.")
        return
    for i, producto in enumerate(productos):
        print(f"  {i + 1}. {producto}")
    print(f"\nPlatos disponibles: {restaurante.contar_productos()}")


def registrar_usuario(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Registrar cliente ---")
    identificacion = pedir_texto("Identificacion: ")
    nombre = pedir_texto("Nombre completo: ")
    correo = pedir_texto("Correo electronico: ")
    try:
        usuario = Usuario(identificacion, nombre, correo)
        if restaurante.registrar_usuario(usuario):
            print("Cliente registrado.")
            guardar_usuarios(archivo, restaurante)
        else:
            print("La identificacion ya esta registrada.")
    except ValueError as error:
        print(f"Dato invalido: {error}")


def buscar_usuario(restaurante: Restaurante) -> None:
    print("\n--- Buscar cliente ---")
    identificacion = pedir_texto("Identificacion: ")
    resultado = restaurante.buscar_usuario(identificacion)
    print(resultado if resultado else "Cliente no encontrado.")


def actualizar_usuario(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Actualizar cliente ---")
    identificacion = pedir_texto("Identificacion: ")
    if restaurante.buscar_usuario(identificacion) is None:
        print("Cliente no encontrado.")
        return
    try:
        nuevo_nombre = pedir_texto("Nuevo nombre: ")
        nuevo_correo = pedir_texto("Nuevo correo: ")
        if restaurante.actualizar_usuario(identificacion, nuevo_nombre, nuevo_correo):
            print("Cliente actualizado.")
            guardar_usuarios(archivo, restaurante)
        else:
            print("No se pudo actualizar.")
    except ValueError as error:
        print(f"Dato invalido: {error}")


def eliminar_usuario(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Eliminar cliente ---")
    identificacion = pedir_texto("Identificacion: ")
    if restaurante.eliminar_usuario(identificacion):
        print("Cliente eliminado.")
        guardar_usuarios(archivo, restaurante)
    else:
        print("Cliente no encontrado.")


def listar_usuarios(restaurante: Restaurante) -> None:
    print("\n--- Clientes registrados ---")
    usuarios = restaurante.listar_usuarios()
    if not usuarios:
        print("Sin clientes registrados.")
        return
    for i, usuario in enumerate(usuarios):
        print(f"  {i + 1}. {usuario}")
    print(f"\nTotal de clientes: {len(usuarios)}")


def realizar_venta(restaurante: Restaurante, archivo: ArchivoServicio) -> None:
    print("\n--- Registrar pedido ---")
    identificacion = pedir_texto("Identificacion del cliente: ")
    codigo = pedir_texto("Codigo del plato: ")
    try:
        cantidad = pedir_entero("Cantidad de pedido: ")
        producto = restaurante.buscar_producto(codigo)
        if producto:
            print(f"Disponibles de '{producto.nombre}': {producto.stock} unidad(es)")
        if restaurante.vender_producto(codigo, identificacion, cantidad):
            actualizado = restaurante.buscar_producto(codigo)
            print("Pedido registrado con exito.")
            print(f"Stock restante: {actualizado.stock if actualizado else 'N/D'}")
            guardar_ventas(archivo, restaurante)
            guardar_productos(archivo, restaurante)
        else:
            print("Pedido rechazado. Verifique que el cliente, el plato, la cantidad y el stock sean validos.")
    except ValueError as error:
        print(f"Dato invalido: {error}")


def consultar_ventas_usuario(restaurante: Restaurante) -> None:
    print("\n--- Pedidos por cliente ---")
    identificacion = pedir_texto("Identificacion del cliente: ")
    if restaurante.buscar_usuario(identificacion) is None:
        print("Cliente no encontrado.")
        return
    ventas = restaurante.consultar_ventas_usuario(identificacion)
    if not ventas:
        print("Este cliente no tiene pedidos registrados.")
        return
    print(f"Pedidos de '{identificacion}':")
    for i, venta in enumerate(ventas):
        producto = restaurante.buscar_producto(venta.producto_codigo)
        nombre = producto.nombre if producto else "N/D"
        print(f"  {i + 1}. {nombre} ({venta.producto_codigo}) — {venta.cantidad} unidad(es)")
    print(f"\nTotal de pedidos: {len(ventas)}")


def listar_todas_ventas(restaurante: Restaurante) -> None:
    print("\n--- Todos los pedidos ---")
    ventas = restaurante.listar_ventas()
    if not ventas:
        print("No hay pedidos registrados.")
        return
    for i, venta in enumerate(ventas):
        print(f"  {i + 1}. {venta}")
    print(f"\nTotal: {restaurante.contar_ventas()} pedido(s)")


def mostrar_categorias(restaurante: Restaurante) -> None:
    print("\n--- Categorias del menu ---")
    categorias = restaurante.obtener_categorias_registradas()
    if not categorias:
        print("Sin categorias.")
        return
    for cat in sorted(categorias):
        print(f"  >> {cat}")


def main() -> None:
    archivo = ArchivoServicio()
    productos = archivo.cargar_productos()
    usuarios = archivo.cargar_usuarios()
    ventas = archivo.cargar_ventas()

    restaurante = Restaurante(productos, usuarios, ventas)
    print("Bienvenido a Restaurante App.")
    print(
        f"Datos disponibles: {restaurante.contar_productos()} plato(s), "
        f"{len(restaurante.listar_usuarios())} cliente(s), "
        f"{restaurante.contar_ventas()} pedido(s)."
    )

    acciones: dict[str, object] = {
        "1":  lambda: registrar_producto(restaurante, archivo),
        "2":  lambda: buscar_producto(restaurante),
        "3":  lambda: actualizar_producto(restaurante, archivo),
        "4":  lambda: eliminar_producto(restaurante, archivo),
        "5":  lambda: listar_productos(restaurante),
        "6":  lambda: registrar_usuario(restaurante, archivo),
        "7":  lambda: buscar_usuario(restaurante),
        "8":  lambda: actualizar_usuario(restaurante, archivo),
        "9":  lambda: eliminar_usuario(restaurante, archivo),
        "10": lambda: listar_usuarios(restaurante),
        "11": lambda: realizar_venta(restaurante, archivo),
        "12": lambda: consultar_ventas_usuario(restaurante),
        "13": lambda: listar_todas_ventas(restaurante),
        "14": lambda: mostrar_categorias(restaurante),
    }

    while True:
        mostrar_menu()
        opcion = pedir_texto("\nOpcion elegida: ")
        if opcion == "0":
            print("Hasta pronto.")
            break
        accion = acciones.get(opcion)
        if accion is None:
            print("Opcion no valida, intente de nuevo.")
        else:
            accion()


if __name__ == "__main__":
    main()
