import json
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
    def __init__(self, ruta_datos: str = "datos") -> None:
        self._ruta_datos = Path(ruta_datos)
        self._ruta_productos = self._ruta_datos / "productos.json"
        self._ruta_usuarios = self._ruta_datos / "usuarios.json"
        self._ruta_ventas = self._ruta_datos / "ventas.json"

    def cargar_productos(self) -> list[Producto]:
        datos = self._leer_lista(self._ruta_productos, "productos")
        productos: list[Producto] = []
        for item in datos:
            if not isinstance(item, dict):
                print("Se omitio un registro de producto con formato incorrecto.")
                continue
            try:
                producto = Producto(
                    item["codigo"],
                    item["nombre"],
                    item["precio"],
                    item["categoria"],
                    item.get("es_vegetariano", False),
                    item.get("stock", 0),
                )
                productos.append(producto)
            except KeyError:
                print("Se omitio un producto por campos faltantes.")
            except ValueError as error:
                print(f"Producto omitido por dato invalido: {error}")
        return productos

    def guardar_productos(self, productos: list[Producto]) -> bool:
        return self._guardar_lista(self._ruta_productos, [p.convertir_a_diccionario() for p in productos], "productos")

    def cargar_usuarios(self) -> list[Usuario]:
        datos = self._leer_lista(self._ruta_usuarios, "usuarios")
        usuarios: list[Usuario] = []
        for item in datos:
            if not isinstance(item, dict):
                print("Se omitio un registro de usuario con formato incorrecto.")
                continue
            try:
                usuarios.append(Usuario(item["identificacion"], item["nombre"], item["correo"]))
            except KeyError:
                print("Se omitio un usuario por campos faltantes.")
            except ValueError as error:
                print(f"Usuario omitido por dato invalido: {error}")
        return usuarios

    def guardar_usuarios(self, usuarios: list[Usuario]) -> bool:
        return self._guardar_lista(self._ruta_usuarios, [u.convertir_a_diccionario() for u in usuarios], "usuarios")

    def cargar_ventas(self) -> list[Venta]:
        datos = self._leer_lista(self._ruta_ventas, "ventas")
        ventas: list[Venta] = []
        for item in datos:
            if not isinstance(item, dict):
                print("Se omitio un registro de venta con formato incorrecto.")
                continue
            try:
                ventas.append(Venta(item["usuario_id"], item["producto_codigo"], item["cantidad"]))
            except KeyError:
                print("Se omitio una venta por campos faltantes.")
            except ValueError as error:
                print(f"Venta omitida por dato invalido: {error}")
        return ventas

    def guardar_ventas(self, ventas: list[Venta]) -> bool:
        return self._guardar_lista(self._ruta_ventas, [v.convertir_a_diccionario() for v in ventas], "ventas")

    def _leer_lista(self, ruta: Path, nombre: str) -> list:
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"El contenido de {nombre} no es JSON valido. Se usara lista vacia.")
            return []
        except PermissionError:
            print(f"Permiso denegado para leer {nombre}.")
            return []
        if not isinstance(datos, list):
            print(f"El archivo {nombre} debe contener una lista JSON.")
            return []
        return datos

    def _guardar_lista(self, ruta: Path, datos: list, nombre: str) -> bool:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"Permiso denegado para guardar {nombre}.")
            return False
