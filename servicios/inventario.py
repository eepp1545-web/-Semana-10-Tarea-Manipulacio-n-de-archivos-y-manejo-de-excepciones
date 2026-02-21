# servicios/inventario.py

from __future__ import annotations
from modelos.producto import Producto


class Inventario:
    """
    Gestiona una lista de productos y operaciones básicas: agregar, eliminar,
    actualizar, buscar y listar.

    MEJORA: Persistencia en archivo de texto (inventario.txt) + manejo de excepciones.
    """

    def __init__(self, ruta_archivo: str = "inventario.txt"):
        self.__productos: list[Producto] = []
        self.__ruta = ruta_archivo

        # Al iniciar, intentamos cargar el inventario desde archivo
        ok, msg = self.__cargar_desde_archivo()
        # Guardamos un mensaje por si main quiere mostrarlo
        self.ultimo_estado_archivo = msg
        self.ultimo_ok_archivo = ok

    def __buscar_por_id(self, producto_id: str) -> Producto | None:
        for p in self.__productos:
            if p.get_id() == producto_id:
                return p
        return None

    # --------------------------
    # Persistencia en archivo
    # --------------------------
    def __asegurar_archivo_existe(self) -> tuple[bool, str]:
        """
        Verifica si el archivo existe; si no existe, lo crea vacío.
        Maneja FileNotFoundError y PermissionError.
        """
        try:
            # Abrir en modo append crea el archivo si no existe
            with open(self.__ruta, "a", encoding="utf-8"):
                pass
            return True, f"Archivo listo: {self.__ruta}"
        except PermissionError:
            return False, f"ERROR: Sin permisos para crear/usar el archivo '{self.__ruta}'."
        except OSError as e:
            return False, f"ERROR: No se pudo preparar el archivo '{self.__ruta}': {e}"

    def __cargar_desde_archivo(self) -> tuple[bool, str]:
        """
        Carga productos desde el archivo y reconstruye la lista en memoria.
        Si hay líneas corruptas, las omite y reporta cuántas.
        """
        ok_arch, msg_arch = self.__asegurar_archivo_existe()
        if not ok_arch:
            return False, msg_arch

        corruptas = 0
        cargados = 0
        productos_tmp: list[Producto] = []
        ids_vistos: set[str] = set()

        try:
            with open(self.__ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    try:
                        p = Producto.from_line(linea)
                        # Evitar IDs duplicados dentro del archivo
                        if p.get_id() in ids_vistos:
                            corruptas += 1
                            continue
                        ids_vistos.add(p.get_id())
                        productos_tmp.append(p)
                        cargados += 1
                    except ValueError:
                        corruptas += 1

            self.__productos = productos_tmp

            if corruptas > 0:
                return True, f"Inventario cargado ({cargados}) con {corruptas} línea(s) corrupta(s) omitida(s)."
            return True, f"Inventario cargado correctamente: {cargados} producto(s)."

        except PermissionError:
            return False, f"ERROR: Sin permisos de lectura para '{self.__ruta}'."
        except OSError as e:
            return False, f"ERROR: Fallo leyendo '{self.__ruta}': {e}"

    def __guardar_a_archivo(self) -> tuple[bool, str]:
        """
        Guarda TODO el inventario actual en el archivo (reescritura completa).
        Si falla por permisos o error del sistema, devuelve (False, mensaje).
        """
        ok_arch, msg_arch = self.__asegurar_archivo_existe()
        if not ok_arch:
            return False, msg_arch

        try:
            with open(self.__ruta, "w", encoding="utf-8") as f:
                for p in self.__productos:
                    f.write(p.to_line() + "\n")
            return True, f"Cambios guardados en '{self.__ruta}'."
        except PermissionError:
            return False, f"ERROR: Sin permisos de escritura en '{self.__ruta}'."
        except OSError as e:
            return False, f"ERROR: Fallo escribiendo '{self.__ruta}': {e}"

    # --------------------------
    # Operaciones del inventario
    # (ahora devuelven (bool, str))
    # --------------------------
    def anadir_producto(self, producto: Producto) -> tuple[bool, str]:
        if self.__buscar_por_id(producto.get_id()) is not None:
            return False, "No se pudo agregar: el ID ya existe."

        self.__productos.append(producto)
        ok, msg = self.__guardar_a_archivo()
        self.ultimo_ok_archivo = ok
        self.ultimo_estado_archivo = msg

        if ok:
            return True, f"Producto agregado. {msg}"
        return False, f"Producto agregado en memoria, pero NO se pudo guardar. {msg}"

    def eliminar_producto(self, producto_id: str) -> tuple[bool, str]:
        producto = self.__buscar_por_id(producto_id)
        if producto is None:
            return False, "No se encontró un producto con ese ID."

        self.__productos.remove(producto)
        ok, msg = self.__guardar_a_archivo()
        self.ultimo_ok_archivo = ok
        self.ultimo_estado_archivo = msg

        if ok:
            return True, f"Producto eliminado. {msg}"
        return False, f"Producto eliminado en memoria, pero NO se pudo guardar. {msg}"

    def actualizar_producto(
        self,
        producto_id: str,
        nueva_cantidad: int | None = None,
        nuevo_precio: float | None = None,
    ) -> tuple[bool, str]:
        producto = self.__buscar_por_id(producto_id)
        if producto is None:
            return False, "No se encontró un producto con ese ID."

        if nueva_cantidad is not None:
            producto.set_cantidad(nueva_cantidad)
        if nuevo_precio is not None:
            producto.set_precio(nuevo_precio)

        ok, msg = self.__guardar_a_archivo()
        self.ultimo_ok_archivo = ok
        self.ultimo_estado_archivo = msg

        if ok:
            return True, f"Producto actualizado. {msg}"
        return False, f"Producto actualizado en memoria, pero NO se pudo guardar. {msg}"

    def buscar_por_nombre(self, texto: str) -> list[Producto]:
        texto = texto.strip().lower()
        if not texto:
            return []
        resultados: list[Producto] = []
        for p in self.__productos:
            if texto in p.get_nombre().lower():
                resultados.append(p)
        return resultados

    def listar_productos(self) -> list[Producto]:
        return list(self.__productos)