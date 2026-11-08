# Importamos ABC y abstractmethod para crear una clase base abstracta.
from abc import ABC, abstractmethod


# La clase Entidad define una estructura común que deben implementar las entidades del sistema.
class Entidad(ABC):

    # Este método es abstracto, por lo que todas las clases hijas deben definirlo.
    @abstractmethod
    def mostrar_informacion(self):
        # La implementación concreta se define en cada subclase.
        pass