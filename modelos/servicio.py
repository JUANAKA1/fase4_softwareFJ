from abc import ABC, abstractmethod
from modelos.entidad import Entidad


# La clase abstracta obliga a cada servicio especializado a implementar estas operaciones.
class Servicio(Entidad, ABC):
    """Contrato común de los servicios ofrecidos por Software FJ."""

    @abstractmethod
    def calcular_costo(self, impuesto=0, descuento=0):
        """Calcula el costo aplicando, opcionalmente, impuesto y descuento."""

    @abstractmethod
    def describir(self):
        """Devuelve una descripción legible del servicio."""

    @abstractmethod
    def validar_parametros(self):
        """Valida los datos específicos requeridos por el servicio."""

    def mostrar_informacion(self):
        # Reutiliza la descripción concreta como información general del servicio.
        return self.describir()