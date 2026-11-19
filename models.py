import os
from abc import ABC, abstractmethod
import pymysql


def consultar(sql, params=(), uno=False):
    """Ejecuta una consulta en MySQL y devuelve filas (o una sola)."""
    con = pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "portfolio"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )
    try:
        with con.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone() if uno else cur.fetchall()
    finally:
        con.close()


# POO - ABSTRACCIÓN: Elemento es una clase abstracta, no se usa directo.
# Define qué deben tener todos los ítems del portfolio.
class Elemento(ABC):
    TABLA = ""
    CAMPOS = []

    def __init__(self, datos):
        # POO - ENCAPSULAMIENTO: los datos son privados (__datos),
        # solo se leen con get() o con la property id.
        self.__datos = datos

    def get(self, campo):
        return self.__datos.get(campo)

    @property
    def id(self):
        return self.__datos["id"]

    @abstractmethod
    def titulo_visible(self):
        """Cada hijo decide cuál es su título."""

    @abstractmethod
    def detalle(self):
        """Cada hijo decide qué detalle muestra."""

    @classmethod
    def listar(cls):
        filas = consultar(f"SELECT * FROM {cls.TABLA} ORDER BY id")
        return [cls(f) for f in filas]

    @classmethod
    def crear(cls, form):
        cols = ", ".join(cls.CAMPOS)
        marcas = ", ".join(["%s"] * len(cls.CAMPOS))
        valores = [form.get(c, "").strip() for c in cls.CAMPOS]
        consultar(f"INSERT INTO {cls.TABLA} ({cols}) VALUES ({marcas})", valores)

    @classmethod
    def borrar(cls, item_id):
        consultar(f"DELETE FROM {cls.TABLA} WHERE id = %s", (item_id,))


# POO - HERENCIA: Estudio, Experiencia y Habilidad heredan de Elemento.
# POO - POLIMORFISMO: las tres implementan titulo_visible() y detalle()
# a su manera, y el template las llama igual sin saber de qué clase son.
class Estudio(Elemento):
    TABLA = "estudio"
    CAMPOS = ["institucion", "titulo", "periodo"]

    def titulo_visible(self):
        return self.get("titulo")

    def detalle(self):
        return f"{self.get('institucion')} - {self.get('periodo')}"


class Experiencia(Elemento):
    TABLA = "experiencia"
    CAMPOS = ["empresa", "puesto", "periodo", "descripcion"]

    def titulo_visible(self):
        return self.get("puesto")

    def detalle(self):
        return f"{self.get('empresa')} - {self.get('periodo')}"


class Habilidad(Elemento):
    TABLA = "habilidad"
    CAMPOS = ["nombre", "categoria"]

    def titulo_visible(self):
        return self.get("nombre")

    def detalle(self):
        return self.get("categoria")


class Perfil:
    @staticmethod
    def obtener():
        return consultar("SELECT * FROM perfil WHERE id = 1", uno=True)

    @staticmethod
    def guardar(f):
        consultar(
            "UPDATE perfil SET nombre=%s, titulo=%s, bio=%s, email=%s, github=%s, linkedin=%s WHERE id=1",
            (f.nombre.data, f.titulo.data, f.bio.data, f.email.data, f.github.data, f.linkedin.data),
        )
