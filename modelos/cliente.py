# Importamos la clase base abstracta Entidad para que Cliente herede su comportamiento.
from modelos.entidad import Entidad


# La clase Cliente representa a una persona o usuario con datos básicos.
class Cliente(Entidad):

    # Constructor de la clase; inicializa los atributos principales del cliente.
    def __init__(self, nombre, identificacion, correo):
        # Se asignan los valores usando los setters para validar la información.
        self.nombre = nombre
        self.identificacion = identificacion
        self.correo = correo

    # Getter del nombre.
    @property
    def nombre(self):
        return self.__nombre

    # Setter del nombre con validación.
    @nombre.setter
    def nombre(self, nuevo_nombre):
        # El nombre no puede quedar vacío.
        if not nuevo_nombre:
            raise ValueError("El nombre no puede estar vacío")
        self.__nombre = nuevo_nombre

    # Getter de la identificación.
    @property
    def identificacion(self):
        return self.__identificacion

    # Setter de la identificación con validación.
    @identificacion.setter
    def identificacion(self, nueva_identificacion):
        # La identificación no puede estar vacía.
        if not nueva_identificacion:
            raise ValueError("La identificación no puede estar vacía")
        self.__identificacion = nueva_identificacion

    # Getter del correo.
    @property
    def correo(self):
        return self.__correo

    # Setter del correo con validación del formato.
    @correo.setter
    def correo(self, nuevo_correo):
        # No se permite un correo vacío.
        if not nuevo_correo:
            raise ValueError("El correo no puede estar vacío")

        # Se valida que tenga un formato básico con '@' y '.' para ser válido.
        if "@" not in nuevo_correo or "." not in nuevo_correo:
            raise ValueError("El correo no tiene un formato válido")

        self.__correo = nuevo_correo

    # Método para mostrar la información del cliente en pantalla.
    def mostrar_informacion(self):
        print(f"Nombre: {self.__nombre}")
        print(f"Identificación: {self.__identificacion}")
        print(f"Correo: {self.__correo}")