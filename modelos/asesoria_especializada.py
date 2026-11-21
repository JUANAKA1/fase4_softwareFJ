from excepciones.errores_personalizados import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    ParametroFaltanteError,
)
from modelos.servicio import Servicio
from utilidades.logger import registrar_error, registrar_evento


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para asesorías técnicas o profesionales."""

    def __init__(self, area=None, especialista=None, costo_hora=None, nivel="Básico"):
        # Se validan los atributos al construir el servicio.
        self.area = area
        self.especialista = especialista
        self.costo_hora = costo_hora
        self.nivel = nivel

    @property
    def area(self):
        return self.__area

    @area.setter
    def area(self, valor):
        # El área de asesoría es obligatoria y debe ser texto.
        if valor is None:
            mensaje = "Falta el área de la asesoría."
            registrar_error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if not isinstance(valor, str) or not valor.strip():
            mensaje = "El área de la asesoría debe ser un texto válido."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__area = " ".join(valor.split())

    @property
    def especialista(self):
        return self.__especialista

    @especialista.setter
    def especialista(self, valor):
        # El nombre del especialista es obligatorio y debe ser texto.
        if valor is None:
            mensaje = "Falta el nombre del especialista."
            registrar_error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if not isinstance(valor, str) or not valor.strip():
            mensaje = "El nombre del especialista debe ser un texto válido."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__especialista = " ".join(valor.split())

    @property
    def costo_hora(self):
        return self.__costo_hora

    @costo_hora.setter
    def costo_hora(self, valor):
        # El costo por hora debe ser un número positivo.
        if valor is None:
            mensaje = "Falta el costo por hora de la asesoría."
            registrar_error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            mensaje = "El costo por hora debe ser un número mayor que cero."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__costo_hora = float(valor)

    @property
    def nivel(self):
        return self.__nivel

    @nivel.setter
    def nivel(self, valor):
        # El nivel permite clasificar la asesoría; se restringe a valores conocidos.
        niveles_validos = {"Básico", "Intermedio", "Avanzado"}
        if valor is None:
            mensaje = "Falta el nivel de la asesoría."
            registrar_error(mensaje)
            raise ParametroFaltanteError(mensaje)
        if not isinstance(valor, str) or valor.strip() not in niveles_validos:
            mensaje = "El nivel debe ser Básico, Intermedio o Avanzado."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)
        self.__nivel = valor.strip()

    def validar_parametros(self):
        """Valida los parámetros específicos de la asesoría especializada."""
        try:
            # Se revalidan los atributos actuales para confirmar que siguen siendo válidos.
            self.area = self.__area
            self.especialista = self.__especialista
            self.costo_hora = self.__costo_hora
            self.nivel = self.__nivel
        except (ParametroFaltanteError, DatosInvalidosError) as error:
            # Encadenamiento de excepción: se conserva la causa original.
            raise DatosInvalidosError(
                "Los parámetros de la asesoría no son válidos."
            ) from error
        else:
            registrar_evento(f"Parámetros validados para asesoría en '{self.__area}'.")
            return True

    def calcular_costo(self, impuesto=0, descuento=0, horas=1, recargo_nivel=0):
        """Calcula el costo de la asesoría.

        Método sobrecargado por parámetros opcionales:
        - calcular_costo()
        - calcular_costo(impuesto, descuento)
        - calcular_costo(impuesto, descuento, horas)
        - calcular_costo(impuesto, descuento, horas, recargo_nivel)
        """
        # Validaciones de entrada para evitar cálculos inválidos.
        if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:
            mensaje = "Las horas de asesoría deben ser mayores que cero."
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
        if isinstance(recargo_nivel, bool) or not isinstance(recargo_nivel, (int, float)) or recargo_nivel < 0:
            mensaje = "El recargo por nivel no puede ser negativo."
            registrar_error(mensaje)
            raise DatosInvalidosError(mensaje)

        try:
            # Se calcula el costo incluyendo horas, recargo, impuesto y descuento.
            costo_base = (self.__costo_hora * horas) + recargo_nivel
            costo_final = costo_base * (1 + impuesto) * (1 - descuento)

            # Control de consistencia del resultado final.
            if costo_final < 0:
                raise CalculoInconsistenteError(
                    "El costo calculado de la asesoría no puede ser negativo."
                )
        except CalculoInconsistenteError:
            registrar_error("Cálculo inconsistente en AsesoriaEspecializada.")
            raise
        except Exception as error:
            # Encadenamiento ante errores inesperados durante el cálculo.
            registrar_error(f"Error inesperado al calcular costo de asesoría: {error}")
            raise CalculoInconsistenteError(
                "No fue posible calcular el costo de la asesoría."
            ) from error
        else:
            registrar_evento(
                f"Costo de asesoría calculado para '{self.__area}': {costo_final:.2f}"
            )
            return round(costo_final, 2)

    def describir(self):
        """Devuelve una descripción legible del servicio de asesoría."""
        descripcion = (
            f"Servicio: Asesoría especializada\n"
            f"Área: {self.__area}\n"
            f"Especialista: {self.__especialista}\n"
            f"Nivel: {self.__nivel}\n"
            f"Costo por hora: ${self.__costo_hora:,.2f}"
        )
        registrar_evento(f"Descripción generada para asesoría '{self.__area}'.")
        return descripcion

    def mostrar_informacion(self):
        # Muestra y retorna la descripción para reutilizarla en reportes o pruebas.
        informacion = self.describir()
        print(informacion)
        return informacion
