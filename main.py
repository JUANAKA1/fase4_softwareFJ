
# Importamos la clase Cliente desde el módulo correspondiente.
from modelos.cliente import Cliente
from modelos.servicio import Servicio

# Creamos un cliente válido para probar la clase.
cliente1 = Cliente(
    "Carlos Pérez",
    "123456789",
    "carlos@gmail.com"
)

# Mostramos la información inicial del cliente.
cliente1.mostrar_informacion()

# Cambiamos el correo del cliente para verificar la actualización.
cliente1.correo = "nuevo@gmail.com"

# Mostramos el nuevo valor del correo en pantalla.
print("\nCorreo actualizado:")
print(cliente1.correo)

# Intentamos asignar un correo inválido para comprobar la validación.
try:
    cliente1.correo = "correoIncorrecto"
except ValueError as error:
    # Capturamos la excepción y la mostramos como mensaje de error.
    print(f"Error: {error}")



servicio1 = Servicio()