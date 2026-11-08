from modelos.cliente import Cliente


# Crear un objeto de tipo Cliente
cliente1 = Cliente(
    "Carlos Pérez",
    "123456789",
    "carlos@gmail.com"
)

# Mostrar información del cliente
cliente1.mostrar_informacion()