# 🍽️ restaurante_app — Semana 11

**Estudiante:** Dayana Valeria Lema Saldaña  
**Asignatura:** Programación Orientada a Objetos — Universidad Estatal Amazónica  
**Entrega:** Semana 11 · Colecciones aplicadas a relaciones y operaciones

---

## 📌 ¿Qué hace este sistema?

`restaurante_app` es una aplicación de consola que permite gestionar el menú, los clientes y los pedidos de un restaurante. En esta semana se incorporó la operación de **venta**, que relaciona un cliente (`Usuario`) con un plato del menú (`Producto`) y genera un registro (`Venta`) que queda guardado en un archivo JSON.

Cada `Producto` indica si es **vegetariano** o no, y los `Usuario` se registran con su correo electrónico. Los datos se conservan entre sesiones gracias a tres archivos JSON independientes.

---

## 🗂️ Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md
```

---

## 🧩 ¿Para qué sirve cada parte?

- **`producto.py`** — representa un plato del menú con código, nombre, precio, categoría (PRINCIPAL, GUARNICION, SOPA, JUGO, POSTRE), indicador vegetariano y stock disponible.
- **`usuario.py`** — representa un cliente registrado con identificación, nombre y correo electrónico. El correo se valida para que contenga `@`.
- **`venta.py`** — representa la relación entre un cliente y un plato. Guarda el ID del usuario, el código del producto y la cantidad pedida.
- **`restaurante.py`** — contiene las tres colecciones y toda la lógica del negocio: registro, búsqueda, actualización, eliminación, ventas y consultas.
- **`archivo_servicio.py`** — lee y escribe los tres archivos JSON con manejo específico de errores.
- **`main.py`** — coordina el menú de consola y delega todo al servicio. No toca las colecciones directamente.

---

## 📦 Control de stock

El atributo `stock` de `Producto` indica las unidades disponibles del plato. Para procesar un pedido el sistema verifica:

- ✅ El cliente existe en la colección de usuarios.
- ✅ El plato existe en la colección de productos.
- ✅ La cantidad solicitada es mayor que cero.
- ✅ El stock del plato es suficiente para cubrir el pedido.

Si alguna condición falla, el pedido se rechaza y ningún archivo se modifica. El stock nunca queda en negativo.

---

## 🔗 Relación Usuario → Producto a través de Venta

```
Cliente registrado
       ↓
Plato del menú con stock >= cantidad
       ↓
Crear Venta(usuario_id, producto_codigo, cantidad)
       ↓
Agregar a la colección _ventas
       ↓
Descontar stock del Producto
       ↓
Guardar ventas.json y productos.json
```

---

## 💾 Persistencia de datos

| Operación | Archivos actualizados |
|---|---|
| Registrar / modificar / eliminar producto | `productos.json` |
| Registrar / modificar / eliminar usuario | `usuarios.json` |
| Realizar una venta exitosa | `ventas.json` + `productos.json` |

Al iniciar el programa, las tres colecciones se recuperan desde sus archivos y se reconstruyen como objetos del dominio.

---

## ⚠️ Excepciones manejadas

| Excepción | Causa | Respuesta del sistema |
|---|---|---|
| `FileNotFoundError` | El JSON no existe aún | Colección vacía, programa continúa |
| `json.JSONDecodeError` | Archivo con contenido inválido | Lista vacía, muestra aviso |
| `PermissionError` | Sin acceso al archivo | Aviso, sin caída del programa |
| `KeyError` | Campo faltante en un registro | Ese registro se omite |
| `ValueError` | Dato inválido en modelo | Operación cancelada con mensaje |

---

## ▶️ Cómo ejecutar

```bash
cd restaurante_app
python main.py
```

---

## 🧪 Pruebas realizadas

- **Pedido válido:** se registró un cliente con correo y un plato vegetariano con stock 12. Se solicitaron 3 unidades; el sistema confirmó y actualizó el stock a 9. Al reiniciar, los datos se recuperaron correctamente.

- **Stock insuficiente:** se intentó pedir 20 unidades del mismo plato (stock 9). El sistema rechazó la operación sin modificar ningún archivo.

- **Correo inválido:** se intentó registrar un cliente con un correo sin `@`. El sistema lanzó `ValueError` y no guardó el registro.

- **Persistencia:** tras cerrar y volver a abrir el programa, los tres archivos JSON conservaron todos los registros y el stock actualizado.
