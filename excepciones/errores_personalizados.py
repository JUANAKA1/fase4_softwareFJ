class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""


class DatosInvalidosError(SoftwareFJError, ValueError):
    """Se utiliza cuando los datos ingresados no son válidos."""


class ClienteNoEncontradoError(SoftwareFJError):
    """Se utiliza cuando un cliente no existe."""


class ServicioNoEncontradoError(SoftwareFJError):
    """Se utiliza cuando un servicio no existe."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se utiliza cuando un servicio no está disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """Se utiliza cuando una reserva tiene datos incorrectos."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se utiliza cuando una operación no está permitida."""


class ParametroFaltanteError(SoftwareFJError):
    """Se utiliza cuando falta un parámetro obligatorio."""


class ReservaNoEncontradaError(SoftwareFJError):
    """Se utiliza cuando una reserva no existe."""


class ArchivoSistemaError(SoftwareFJError):
    """Se utiliza cuando ocurre un problema con un archivo del sistema."""
