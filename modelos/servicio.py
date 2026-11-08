from abc import ABC, abstractmethod
from modelos.entidad import Entidad


class Servicio(Entidad, ABC):

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self):
        pass