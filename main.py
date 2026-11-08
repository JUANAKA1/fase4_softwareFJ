
from modelos.cliente import Cliente

# Crear un cliente válido
cliente1 = Cliente(
    "Carlos Pérez",
    "123456789",
    "carlos@gmail.com"
)

# Mostrar información
cliente1.mostrar_informacion()

# Modificar el correo
cliente1.correo = "nuevo@gmail.com"

print("\nCorreo actualizado:")
print(cliente1.correo)

# Probar correo inválido
try:
    cliente1.correo = "correoIncorrecto"
except ValueError as error:
    print(f"Error: {error}")