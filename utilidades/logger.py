import logging
from pathlib import Path

# La ruta basada en este archivo funciona igual aunque se ejecute main.py desde otra carpeta.
RUTA_LOGS = Path(__file__).resolve().parent.parent / "logs"
RUTA_LOGS.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)
logger.propagate = False

# Evita agregar el mismo archivo varias veces si el módulo se carga de nuevo.
if not any(
    isinstance(handler, logging.FileHandler)
    and Path(handler.baseFilename).resolve() == (RUTA_LOGS / "software_fj.log").resolve()
    for handler in logger.handlers
):
    manejador = logging.FileHandler(
        RUTA_LOGS / "software_fj.log",
        encoding="utf-8",
    )
    manejador.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(manejador)


def registrar_evento(mensaje):
    """Registra un evento normal del sistema, como una operación exitosa."""
    logger.info(mensaje)


def registrar_error(mensaje, *, exc_info=False):
    """Registra un error y, si se solicita, incluye los detalles de la excepción activa."""
    logger.error(mensaje, exc_info=exc_info)
