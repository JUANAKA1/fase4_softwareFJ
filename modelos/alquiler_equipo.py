from excepciones.errores_personalizados import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    ParametroFaltanteError,
)
from modelos.servicio import Servicio
from utilidades.logger import registrar_error, registrar_evento


class AlquilerEquipo(Servicio):
    """Servicio especializado para el alquiler de equipos tecnológicos."""

    def __init__(self, nombre_equipo=None, costo_dia=None, disponible=True):
        # Se validan los datos al crear el objeto para garantizar consistencia.
        self.nombre_equipo = nombre_equipo
        self.costo_dia = costo_dia
        self.disponible = disponible

    @property
    def nombre_equipo(self):
        return self.__nombre_equipo

    @nombre_equipo.setter
    def nombre_equipo(self, valor):
        # Se valida que el nombre del equipo sea un texto no vacío.
        if valor is None:
            mensaje = "Falta el nombre del equipo."
            registrar_error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if not isinstance(valor, str) or not valor.strip():
            mensaje = "El nombre del equipo debe ser un texto válido."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__nombre_equipo = " ".join(valor.split())

    @property
    def costo_dia(self):
        return self.__costo_dia

    @costo_dia.setter
    def costo_dia(self, valor):
        # Se valida que el costo por día sea un número positivo.
        if valor is None:
            mensaje = "Falta el costo por día del equipo."
            registrar_error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            mensaje = "El costo por día debe ser un número mayor que cero."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__costo_dia = float(valor)

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        # La disponibilidad debe ser un valor booleano.
        if not isinstance(valor, bool):
            mensaje = "La disponibilidad debe ser un valor booleano."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__disponible = valor

    def validar_parametros(self):
        """Valida los parámetros específicos del servicio de alquiler de equipos."""
        try:
            # Se reutilizan las validaciones de los setters asignando los valores actuales.
            self.nombre_equipo = self.__nombre_equipo
            self.costo_dia = self.__costo_dia
            self.disponible = self.__disponible
        except (ParametroFaltanteError, DatosInvalidosError) as error:
            # Se encadena la excepción para conservar el contexto del error original.
            raise DatosInvalidosError(
                "Los parámetros del alquiler de equipo no son válidos."
            ) from error
        else:
            # Este bloque se ejecuta solo si no hubo excepciones en la validación.
            registrar_evento(
                f"Parámetros validados para el equipo '{self.__nombre_equipo}'."
            )
            return True

    def calcular_costo(self, impuesto=0, descuento=0, dias=1, tarifa_envio=0):
        """Calcula el costo del alquiler.

        Método sobrecargado por parámetros opcionales:
        - calcular_costo()
        - calcular_costo(impuesto, descuento)
        - calcular_costo(impuesto, descuento, dias)
        - calcular_costo(impuesto, descuento, dias, tarifa_envio)
        """
        # Validación de los parámetros numéricos usados en el cálculo.
        if isinstance(dias, bool) or not isinstance(dias, int) or dias <= 0:
            mensaje = "Los días de alquiler deben ser un entero mayor que cero."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 1:
            mensaje = "El impuesto debe estar entre 0 y 1."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not 0 <= descuento <= 1:
            mensaje = "El descuento debe estar entre 0 y 1."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        if isinstance(tarifa_envio, bool) or not isinstance(tarifa_envio, (int, float)) or tarifa_envio < 0:
            mensaje = "La tarifa de envío no puede ser negativa."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)

        try:
            # Cálculo base: costo por día * días + envío, luego impuesto y descuento.
            costo_base = (self.__costo_dia * dias) + tarifa_envio
            costo_final = costo_base * (1 + impuesto) * (1 - descuento)

            # Se verifica que el resultado sea coherente.
            if costo_final < 0:
                raise CalculoInconsistenteError(
                    "El costo calculado del alquiler no puede ser negativo."
                )
        except CalculoInconsistenteError:
            # Se registra y se propaga el error de cálculo inconsistente.
            registrar_error("Cálculo inconsistente en AlquilerEquipo.")
            raise
        except Exception as error:
            # Cualquier error inesperado se encadena para no perder el contexto.
            registrar_error(f"Error inesperado al calcular costo de alquiler: {error}")
            raise CalculoInconsistenteError(
                "No fue posible calcular el costo del alquiler."
            ) from error
        else:
            registrar_evento(
                f"Costo de alquiler calculado para '{self.__nombre_equipo}': {costo_final:.2f}"
            )
            return round(costo_final, 2)

    def describir(self):
        """Devuelve una descripción legible del servicio de alquiler."""
        estado = "Disponible" if self.__disponible else "No disponible"
        descripcion = (
            f"Servicio: Alquiler de equipo\n"
            f"Equipo: {self.__nombre_equipo}\n"
            f"Costo por día: ${self.__costo_dia:,.2f}\n"
            f"Estado: {estado}"
        )
        registrar_evento(f"Descripción generada para equipo '{self.__nombre_equipo}'.")
        return descripcion

    def mostrar_informacion(self):
        # Muestra y retorna la información para facilitar su reutilización.
        informacion = self.describir()
        print(informacion)
        return informacion
