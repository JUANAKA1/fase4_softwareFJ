from modelos.servicio import Servicio
from datetime import datetime

from excepciones.errores_personalizados import (
    DatosInvalidosError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
)

from utilidades.logger import logger


class ReservaSala(Servicio):
    """Representa un servicio de reserva de salas de Software FJ."""

    def __init__(
        self,
        nombre_sala=None,
        capacidad=None,
        precio_hora=None,
    ):
        self.nombre_sala = nombre_sala
        self.capacidad = capacidad
        self.precio_hora = precio_hora
        self.__reservas = []

    @property
    def nombre_sala(self):
        return self.__nombre_sala

    @nombre_sala.setter
    def nombre_sala(self, valor):
        if valor is None:
            mensaje = "Falta el nombre de la sala."
            logger.error(mensaje)
            raise ParametroFaltanteError(mensaje)

        if not isinstance(valor, str) or not valor.strip():
            mensaje = "El nombre de la sala debe ser un texto válido."
            logger.error(mensaje)
            raise DatosInvalidosError(mensaje)

        self.__nombre_sala = " ".join(valor.split())

    @property
    def capacidad(self):
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, valor):
        if valor is None:
            mensaje = "Falta la capacidad de la sala."
            logger.error(mensaje)
            raise ParametroFaltanteError(mensaje)

        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            mensaje = "La capacidad debe ser un número entero mayor que cero."
            logger.error(mensaje)
            raise DatosInvalidosError(mensaje)

        self.__capacidad = valor

    @property
    def precio_hora(self):
        return self.__precio_hora

    @precio_hora.setter
    def precio_hora(self, valor):
        if valor is None:
            mensaje = "Falta el precio por hora."
            logger.error(mensaje)
            raise ParametroFaltanteError(mensaje)

        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            mensaje = "El precio por hora debe ser un número mayor que cero."
            logger.error(mensaje)
            raise DatosInvalidosError(mensaje)

        self.__precio_hora = float(valor)

    @property
    def reservas(self):
        """Devuelve una copia de las reservas registradas."""
        return self.__reservas.copy()     


    # NUEVO MÉTODO
    def validar_parametros(self):
        """Comprueba que los datos de la sala sean válidos."""
        if not self.nombre_sala:
            raise DatosInvalidosError("El nombre de la sala es obligatorio.")

        if self.capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser mayor que cero.")

        if self.precio_hora <= 0:
            raise DatosInvalidosError("El precio por hora debe ser mayor que cero.")

        logger.info("Parámetros de la sala validados correctamente.")
        return True


    def calcular_costo(self, impuesto=0, descuento=0, duracion_horas=1):
        """Calcula el costo de la reserva según las horas, impuestos y descuentos."""

        if (
            isinstance(duracion_horas, bool)
            or not isinstance(duracion_horas, (int, float))
            or duracion_horas <= 0
        ):
            raise DatosInvalidosError("La duración debe ser mayor que cero.")

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 1:
            raise DatosInvalidosError("El impuesto debe estar entre 0 y 1.")

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not 0 <= descuento <= 1:
            raise DatosInvalidosError("El descuento debe estar entre 0 y 1.")

        costo_base = self.precio_hora * duracion_horas
        costo_final = costo_base * (1 + impuesto) * (1 - descuento)

        logger.info("Costo de reserva calculado correctamente.")
        return round(costo_final, 2)

    def describir(self):
        """Devuelve una descripción detallada del servicio de reserva."""
        descripcion = (
            f"Servicio: Reserva de sala\n"
            f"Nombre de la sala: {self.nombre_sala}\n"
            f"Capacidad: {self.capacidad} personas\n"
            f"Precio por hora: ${self.precio_hora:,.2f}"
        )

        logger.info("Descripción de la sala generada.")
        return descripcion

    def mostrar_informacion(self):
        """Muestra la información completa de la sala."""
        informacion = self.describir()
        print(informacion)
        return informacion

    def verificar_disponibilidad(self, fecha_inicio, fecha_fin):
        """Comprueba si la sala está libre durante el horario solicitado."""

        if not isinstance(fecha_inicio, datetime) or not isinstance(fecha_fin, datetime):
            raise DatosInvalidosError("Las fechas deben ser objetos datetime.")

        if fecha_inicio >= fecha_fin:
            raise ReservaInvalidaError(
                "La fecha de inicio debe ser anterior a la fecha de finalización."
            )

        for reserva in self.__reservas:
            inicio_existente = reserva["fecha_inicio"]
            fin_existente = reserva["fecha_fin"]

            if fecha_inicio < fin_existente and fecha_fin > inicio_existente:
                logger.warning("La sala no está disponible en ese horario.")
                raise ServicioNoDisponibleError(
                    f"La sala {self.nombre_sala} ya está reservada en ese horario."
                )

        logger.info("La sala está disponible para el horario solicitado.")
        return True

    def registrar_reserva(
        self, fecha_inicio, fecha_fin, cantidad_personas
    ):
        """Registra una reserva si hay disponibilidad y capacidad."""

        try:
            self.validar_parametros()
            self.validar_capacidad(cantidad_personas)
            self.verificar_disponibilidad(fecha_inicio, fecha_fin)

            nueva_reserva = {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "cantidad_personas": cantidad_personas
            }

            self.__reservas.append(nueva_reserva)

            logger.info(
                f"Reserva registrada correctamente para la sala {self.nombre_sala}."
            )

            return nueva_reserva

        except (
            DatosInvalidosError,
            ReservaInvalidaError,
            ServicioNoDisponibleError
        ) as error:
            logger.error(f"No se pudo registrar la reserva: {error}")
            raise
    def validar_capacidad(self, cantidad_personas):
        """Comprueba que la cantidad de personas no supere la capacidad."""

        if (
            isinstance(cantidad_personas, bool)
            or not isinstance(cantidad_personas, int)
            or cantidad_personas <= 0
        ):
            raise DatosInvalidosError(
                "La cantidad de personas debe ser un entero mayor que cero."
            )

        if cantidad_personas > self.capacidad:
            mensaje = (
                f"La sala admite máximo {self.capacidad} personas. "
                f"Se solicitaron {cantidad_personas}."
            )
            logger.error(mensaje)
            raise ReservaInvalidaError(mensaje)

        logger.info("La capacidad de la sala es suficiente.")
        return True
    