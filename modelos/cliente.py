from modelos.entidad import Entidad


class Cliente(Entidad):

    def __init__(self, nombre, identificacion, correo):
        self.nombre = nombre
        self.identificacion = identificacion
        self.correo = correo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if not nuevo_nombre:
            raise ValueError("El nombre no puede estar vacío")
        self.__nombre = nuevo_nombre

    @property
    def identificacion(self):
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, nueva_identificacion):
        if not nueva_identificacion:
            raise ValueError("La identificación no puede estar vacía")
        self.__identificacion = nueva_identificacion

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, nuevo_correo):
        if not nuevo_correo:
            raise ValueError("El correo no puede estar vacío")

        if "@" not in nuevo_correo or "." not in nuevo_correo:
            raise ValueError("El correo no tiene un formato válido")

        self.__correo = nuevo_correo

    def mostrar_informacion(self):
        print(f"Nombre: {self.__nombre}")
        print(f"Identificación: {self.__identificacion}")
        print(f"Correo: {self.__correo}")