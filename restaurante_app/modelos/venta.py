class Venta:
    def __init__(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int,
    ) -> None:
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

    @property
    def usuario_id(self) -> str:
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificacion del cliente no puede estar vacia.")
        self._usuario_id = valor.strip()

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El codigo del plato no puede estar vacio.")
        self._producto_codigo = valor.strip().upper()

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        try:
            cantidad = int(valor)
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un numero entero valido.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser un valor positivo.")
        self._cantidad = cantidad

    def convertir_a_diccionario(self) -> dict:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
        }

    def __str__(self) -> str:
        return (
            f"Cliente: {self.usuario_id} | "
            f"Plato: {self.producto_codigo} | "
            f"Pedido: {self.cantidad} unidad(es)"
        )
