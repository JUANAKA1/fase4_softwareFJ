from modelos.entidad import Entidad


class Cliente(Entidad):

    def __init__(self, nombre, identificacion, correo):
        self.nombre = nombre
        self.identificacion = identificacion
        self.correo = correo

    def mostrar_informacion(self):
        print(f"Nombre: {self.nombre}")
        print(f"Identificación: {self.identificacion}")
        print(f"Correo: {self.correo}")