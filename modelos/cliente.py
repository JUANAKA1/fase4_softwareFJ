import re

from excepciones.errores_personalizados import (
    DatosInvalidosError,
    ParametroFaltanteError,
)
from modelos.entidad import Entidad
from utilidades.logger import logger


class Cliente(Entidad):
    """Representa un cliente y mantiene sus datos validados y encapsulados."""

    def __init__(self, nombre=None, identificacion=None, correo=None):
        # Los setters validan los valores desde la creación y en cada cambio posterior.
        self.nombre = nombre
        self.identificacion = identificacion
        self.correo = correo

    @property
    def nombre(self):
        # Los atributos con doble guion bajo evitan el acceso directo desde fuera.
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = self._validar_texto(nuevo_nombre, "nombre")

    @property
    def identificacion(self):
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, nueva_identificacion):
        # Se distingue entre un parámetro omitido y un valor con formato incorrecto.
        if nueva_identificacion is None:
            mensaje = "Falta el parámetro obligatorio: identificación."
            logger.error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if isinstance(nueva_identificacion, bool) or not isinstance(
            nueva_identificacion, (str, int)
        ):
            mensaje = "La identificación debe ser texto o un número entero."
            logger.error(mensaje)
            raise DatosInvalidosError(mensaje)

        # Guardar la identificación como texto conserva ceros iniciales (por ejemplo, "00123").
        identificacion = str(nueva_identificacion).strip()
        if not identificacion:
            mensaje = "La identificación no puede estar vacía."
            logger.error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__identificacion = identificacion

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, nuevo_correo):
        correo = self._validar_texto(nuevo_correo, "correo")
        # Esta expresión comprueba una estructura básica de correo sin espacios.
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            mensaje = "El correo no tiene un formato válido."
            logger.error(mensaje)
            raise DatosInvalidosError(mensaje)
        # Se normaliza para evitar duplicados causados solo por mayúsculas.
        self.__correo = correo.lower()

    @staticmethod
    def _validar_texto(valor, campo):
        """Comprueba que un dato requerido sea texto y no esté vacío."""
        if valor is None:
            mensaje = f"Falta el parámetro obligatorio: {campo}."
            logger.error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if not isinstance(valor, str):
            mensaje = f"El {campo} debe ser texto."
            logger.error(mensaje)
            raise DatosInvalidosError(mensaje)

        # Unifica espacios y elimina los extremos antes de almacenar el valor.
        valor = " ".join(valor.split())
        if not valor:
            mensaje = f"El {campo} no puede estar vacío."
            logger.error(mensaje)
            raise DatosInvalidosError(mensaje)
        return valor

    def mostrar_informacion(self):
        # Se devuelve el texto además de imprimirlo para permitir reutilizarlo.
        informacion = (
            f"Nombre: {self.__nombre}\n"
            f"Identificación: {self.__identificacion}\n"
            f"Correo: {self.__correo}"
        )
        print(informacion)
        return informacion