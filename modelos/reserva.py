from excepciones.errores_personalizados import (
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaInvalidaError,
)
from modelos.cliente import Cliente
from modelos.servicio import Servicio
from utilidades.logger import registrar_error, registrar_evento


class Reserva:
    """Representa una reserva que integra cliente, servicio, duración y estado."""

    # Estados permitidos para controlar el ciclo de vida de la reserva.
    ESTADOS_VALIDOS = {"PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"}

    def __init__(self, cliente=None, servicio=None, duracion=None, estado="PENDIENTE"):
        # Se validan todos los datos al crear la reserva.
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = estado

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, valor):
        # La reserva debe estar asociada a un objeto Cliente válido.
        if valor is None:
            mensaje = "Falta el cliente de la reserva."
            registrar_error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if not isinstance(valor, Cliente):
            mensaje = "El cliente de la reserva debe ser una instancia de Cliente."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__cliente = valor

    @property
    def servicio(self):
        return self.__servicio

    @servicio.setter
    def servicio(self, valor):
        # La reserva debe estar asociada a un servicio que herede de Servicio.
        if valor is None:
            mensaje = "Falta el servicio de la reserva."
            registrar_error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if not isinstance(valor, Servicio):
            mensaje = "El servicio de la reserva debe ser una instancia de Servicio."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__servicio = valor

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, valor):
        # La duración representa unidades de tiempo (horas/días) según el servicio.
        if valor is None:
            mensaje = "Falta la duración de la reserva."
            registrar_error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            mensaje = "La duración de la reserva debe ser mayor que cero."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__duracion = float(valor)

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        # Solo se permiten estados controlados para evitar inconsistencias.
        if valor is None:
            mensaje = "Falta el estado de la reserva."
            registrar_error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if not isinstance(valor, str) or valor.strip().upper() not in self.ESTADOS_VALIDOS:
            mensaje = f"Estado inválido. Estados permitidos: {', '.join(sorted(self.ESTADOS_VALIDOS))}."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__estado = valor.strip().upper()

    def confirmar(self):
        """Confirma la reserva si se encuentra en estado PENDIENTE."""
        try:
            # Solo una reserva pendiente puede confirmarse.
            if self.__estado != "PENDIENTE":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva en estado {self.__estado}."
                )

            # Antes de confirmar, se validan los parámetros del servicio asociado.
            self.__servicio.validar_parametros()
            self.__estado = "CONFIRMADA"
        except OperacionNoPermitidaError as error:
            # Se registra y se propaga para que el flujo superior decida cómo continuar.
            registrar_error(f"Error al confirmar reserva: {error}")
            raise
        except Exception as error:
            # Encadenamiento de excepciones: se conserva la causa original.
            registrar_error(f"Fallo inesperado al confirmar reserva: {error}")
            raise ReservaInvalidaError(
                "No fue posible confirmar la reserva por un error interno."
            ) from error
        else:
            registrar_evento(
                f"Reserva confirmada para el cliente '{self.__cliente.nombre}'."
            )
            return True
        finally:
            # Este bloque siempre se ejecuta, haya éxito o error.
            registrar_evento(
                f"Intento de confirmación finalizado. Estado actual: {self.__estado}."
            )

    def cancelar(self, motivo="Sin motivo especificado"):
        """Cancela la reserva si no ha sido procesada."""
        try:
            # No se permite cancelar una reserva que ya fue procesada.
            if self.__estado == "PROCESADA":
                raise OperacionNoPermitidaError(
                    "No se puede cancelar una reserva que ya fue procesada."
                )
            if self.__estado == "CANCELADA":
                raise OperacionNoPermitidaError("La reserva ya se encuentra cancelada.")

            if not isinstance(motivo, str) or not motivo.strip():
                raise DatosInvalidosError("El motivo de cancelación debe ser texto válido.")

            self.__estado = "CANCELADA"
        except (OperacionNoPermitidaError, DatosInvalidosError) as error:
            registrar_error(f"Error al cancelar reserva: {error}")
            raise
        else:
            registrar_evento(
                f"Reserva cancelada para '{self.__cliente.nombre}'. Motivo: {motivo.strip()}"
            )
            return True
        finally:
            # Siempre se deja rastro en el log del intento de cancelación.
            registrar_evento(
                f"Intento de cancelación finalizado. Estado actual: {self.__estado}."
            )

    def procesar(self, impuesto=0, descuento=0):
        """Procesa la reserva confirmada y calcula el costo final."""
        try:
            # Solo se pueden procesar reservas confirmadas.
            if self.__estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    f"Solo se pueden procesar reservas confirmadas. Estado actual: {self.__estado}."
                )

            # El costo se calcula usando el método polimórfico del servicio.
            costo = self._calcular_costo_servicio(impuesto=impuesto, descuento=descuento)

            # Si el cálculo fue exitoso, la reserva pasa a estado PROCESADA.
            self.__estado = "PROCESADA"
        except OperacionNoPermitidaError as error:
            registrar_error(f"Error al procesar reserva: {error}")
            raise
        except Exception as error:
            # Se encadena la excepción para mantener la causa técnica original.
            registrar_error(f"Fallo inesperado al procesar reserva: {error}")
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva."
            ) from error
        else:
            registrar_evento(
                f"Reserva procesada para '{self.__cliente.nombre}'. Costo: {costo:.2f}"
            )
            return costo
        finally:
            registrar_evento(
                f"Intento de procesamiento finalizado. Estado actual: {self.__estado}."
            )

    def _calcular_costo_servicio(self, impuesto=0, descuento=0):
        """Calcula el costo según el tipo de servicio, demostrando polimorfismo."""
        # Se intenta usar la firma extendida con duración; si no aplica, se usa la básica.
        try:
            return self.__servicio.calcular_costo(
                impuesto=impuesto, descuento=descuento, duracion_horas=self.__duracion
            )
        except TypeError:
            # Algunos servicios usan nombres de parámetro distintos; se prueban alternativas.
            try:
                return self.__servicio.calcular_costo(
                    impuesto=impuesto, descuento=descuento, dias=int(self.__duracion)
                )
            except TypeError:
                try:
                    return self.__servicio.calcular_costo(
                        impuesto=impuesto, descuento=descuento, horas=self.__duracion
                    )
                except TypeError:
                    # Último recurso: usar la firma básica definida en la clase abstracta.
                    return self.__servicio.calcular_costo(impuesto=impuesto, descuento=descuento)

    def mostrar_informacion(self):
        """Muestra un resumen legible de la reserva."""
        informacion = (
            f"Reserva\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Servicio: {self.__servicio.describir().splitlines()[0]}\n"
            f"Duración: {self.__duracion}\n"
            f"Estado: {self.__estado}"
        )
        print(informacion)
        return informacion
