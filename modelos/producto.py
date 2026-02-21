# modelos/producto.py

class Producto:
    """
    Representa un producto dentro del inventario.
    Incluye atributos básicos, getters/setters y utilidades de serialización.
    """

    SEP = "|"  # Separador para archivo de texto

    def __init__(self, producto_id: str, nombre: str, cantidad: int, precio: float):
        self.__id = producto_id
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # Getters
    def get_id(self) -> str:
        return self.__id

    def get_nombre(self) -> str:
        return self.__nombre

    def get_cantidad(self) -> int:
        return self.__cantidad

    def get_precio(self) -> float:
        return self.__precio

    # Setters
    def set_id(self, producto_id: str) -> None:
        self.__id = producto_id

    def set_nombre(self, nombre: str) -> None:
        self.__nombre = nombre

    def set_cantidad(self, cantidad: int) -> None:
        self.__cantidad = cantidad

    def set_precio(self, precio: float) -> None:
        self.__precio = precio

    # --- Serialización a texto (archivo) ---
    def to_line(self) -> str:
        """
        Convierte el producto a una línea de texto para guardarlo en inventario.txt
        IMPORTANTE: evitamos saltos de línea y el separador en el nombre.
        """
        safe_id = str(self.__id).replace("\n", " ").strip()
        safe_name = str(self.__nombre).replace("\n", " ").replace(self.SEP, "/").strip()
        return f"{safe_id}{self.SEP}{safe_name}{self.SEP}{int(self.__cantidad)}{self.SEP}{float(self.__precio)}"

    @staticmethod
    def from_line(linea: str) -> "Producto":
        """
        Crea un Producto desde una línea del archivo.
        Lanza ValueError si la línea está corrupta.
        """
        parts = linea.strip().split(Producto.SEP)
        if len(parts) != 4:
            raise ValueError("Línea con número de campos incorrecto")

        producto_id = parts[0].strip()
        nombre = parts[1].strip()
        cantidad = int(parts[2].strip())
        precio = float(parts[3].strip())

        if not producto_id or not nombre or cantidad < 0 or precio < 0:
            raise ValueError("Datos inválidos en la línea")

        return Producto(producto_id, nombre, cantidad, precio)

    def __str__(self) -> str:
        return (
            f"ID: {self.__id} | "
            f"Nombre: {self.__nombre} | "
            f"Cantidad: {self.__cantidad} | "
            f"Precio: ${self.__precio:.2f}"
        )