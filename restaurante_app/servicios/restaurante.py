from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    def __init__(
        self,
        productos_iniciales: list[Producto] | None = None,
        usuarios_iniciales: list[Usuario] | None = None,
        ventas_iniciales: list[Venta] | None = None,
    ) -> None:
        self._productos: list[Producto] = productos_iniciales.copy() if productos_iniciales else []
        self._usuarios: list[Usuario] = usuarios_iniciales.copy() if usuarios_iniciales else []
        self._ventas: list[Venta] = ventas_iniciales.copy() if ventas_iniciales else []

    def registrar_producto(self, producto: Producto) -> bool:
        if self.buscar_producto(producto.codigo) is not None:
            return False
        self._productos.append(producto)
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        codigo = codigo.strip().upper()
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def actualizar_producto(self, codigo: str, nuevo_nombre: str, nuevo_precio: float, nueva_categoria: str, nuevo_vegetariano: bool, nuevo_stock: int) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        producto.nombre = nuevo_nombre
        producto.precio = nuevo_precio
        producto.categoria = nueva_categoria
        producto.es_vegetariano = nuevo_vegetariano
        producto.stock = nuevo_stock
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        return True

    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    def contar_productos(self) -> int:
        return len(self._productos)

    def obtener_categorias_registradas(self) -> set[str]:
        return {p.categoria for p in self._productos}

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if self.buscar_usuario(usuario.identificacion) is not None:
            return False
        self._usuarios.append(usuario)
        return True

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        identificacion = identificacion.strip()
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None

    def actualizar_usuario(self, identificacion: str, nuevo_nombre: str, nuevo_correo: str) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        usuario.nombre = nuevo_nombre
        usuario.correo = nuevo_correo
        return True

    def eliminar_usuario(self, identificacion: str) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        self._usuarios.remove(usuario)
        return True

    def listar_usuarios(self) -> list[Usuario]:
        return self._usuarios.copy()

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)
        if usuario is None or producto is None:
            return False
        if cantidad <= 0 or producto.stock < cantidad:
            return False
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        producto.vender(cantidad)
        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> list[Venta]:
        identificacion_usuario = identificacion_usuario.strip()
        ventas_usuario: list[Venta] = []
        for venta in self._ventas:
            if venta.usuario_id == identificacion_usuario:
                ventas_usuario.append(venta)
        return ventas_usuario

    def listar_ventas(self) -> list[Venta]:
        return self._ventas.copy()

    def contar_ventas(self) -> int:
        return len(self._ventas)
