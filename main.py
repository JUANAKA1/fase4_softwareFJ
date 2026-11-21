"""
Punto de entrada del sistema integral de Software FJ.

Este script simula al menos 10 operaciones completas, incluyendo casos válidos
e inválidos, para demostrar el funcionamiento del sistema orientado a objetos,
la validación de datos, el registro de logs y el manejo avanzado de excepciones.
"""

from datetime import datetime

from excepciones.errores_personalizados import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    SoftwareFJError,
)
from modelos.alquiler_equipo import AlquilerEquipo
from modelos.asesoria_especializada import AsesoriaEspecializada
from modelos.cliente import Cliente
from modelos.reserva import Reserva
from modelos.reserva_sala import ReservaSala
from utilidades.logger import registrar_error, registrar_evento


def mostrar_titulo(texto):
    """Imprime un separador visual para identificar cada operación en consola."""
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def main():
    """Ejecuta la simulación completa del sistema."""
    registrar_evento("Inicio de la simulación del sistema Software FJ.")

    # Se almacenan objetos en listas para simular la gestión en memoria.
    clientes = []
    servicios = []
    reservas = []

    # ------------------------------------------------------------------
    # Operación 1: Registro válido de cliente.
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 1: Registro válido de cliente")
    try:
        cliente1 = Cliente("Carlos Pérez", "123456789", "carlos@gmail.com")
        clientes.append(cliente1)
        cliente1.mostrar_informacion()
    except SoftwareFJError as error:
        registrar_error(f"Operación 1 falló: {error}")
        print(f"Error controlado: {error}")
    else:
        # El bloque else se ejecuta solo cuando no ocurre ninguna excepción.
        registrar_evento("Operación 1 completada: cliente registrado correctamente.")
        print("Cliente registrado correctamente.")
    finally:
        # El bloque finally se ejecuta siempre, haya error o no.
        print("Fin de la operación 1.")

    # ------------------------------------------------------------------
    # Operación 2: Registro inválido de cliente (correo incorrecto).
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 2: Registro inválido de cliente - correo incorrecto")
    try:
        cliente_invalido = Cliente("Ana Gómez", "987654321", "correo-invalido")
        clientes.append(cliente_invalido)
    except DatosInvalidosError as error:
        registrar_error(f"Operación 2: dato inválido detectado: {error}")
        print(f"Error controlado: {error}")
    finally:
        print("Fin de la operación 2.")

    # ------------------------------------------------------------------
    # Operación 3: Registro inválido de cliente (parámetro faltante).
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 3: Registro inválido de cliente - parámetro faltante")
    try:
        cliente_faltante = Cliente(nombre="Laura Ruiz", identificacion=None, correo="laura@gmail.com")
        clientes.append(cliente_faltante)
    except ParametroFaltanteError as error:
        registrar_error(f"Operación 3: parámetro faltante: {error}")
        print(f"Error controlado: {error}")
    finally:
        print("Fin de la operación 3.")

    # ------------------------------------------------------------------
    # Operación 4: Creación correcta de servicio - Reserva de sala.
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 4: Creación correcta de servicio - Reserva de sala")
    try:
        sala = ReservaSala(nombre_sala="Sala Principal", capacidad=20, precio_hora=50000)
        sala.validar_parametros()
        servicios.append(sala)
        sala.mostrar_informacion()
    except SoftwareFJError as error:
        registrar_error(f"Operación 4 falló: {error}")
        print(f"Error controlado: {error}")
    else:
        registrar_evento("Operación 4 completada: sala creada correctamente.")
        print("Servicio de sala creado correctamente.")

    # ------------------------------------------------------------------
    # Operación 5: Creación correcta de servicios - Alquiler y Asesoría.
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 5: Creación correcta de servicios - Alquiler y Asesoría")
    try:
        equipo = AlquilerEquipo(nombre_equipo="Proyector Epson", costo_dia=80000, disponible=True)
        asesoria = AsesoriaEspecializada(
            area="Ciberseguridad",
            especialista="María Torres",
            costo_hora=120000,
            nivel="Avanzado",
        )
        # Se validan y almacenan ambos servicios.
        equipo.validar_parametros()
        asesoria.validar_parametros()
        servicios.extend([equipo, asesoria])
        equipo.mostrar_informacion()
        print()
        asesoria.mostrar_informacion()
    except SoftwareFJError as error:
        registrar_error(f"Operación 5 falló: {error}")
        print(f"Error controlado: {error}")
    else:
        registrar_evento("Operación 5 completada: servicios creados correctamente.")

    # ------------------------------------------------------------------
    # Operación 6: Creación incorrecta de servicio (datos inválidos).
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 6: Creación incorrecta de servicio - datos inválidos")
    try:
        equipo_invalido = AlquilerEquipo(nombre_equipo="Laptop", costo_dia=-50000)
        servicios.append(equipo_invalido)
    except DatosInvalidosError as error:
        registrar_error(f"Operación 6: servicio inválido: {error}")
        print(f"Error controlado: {error}")
    finally:
        print("Fin de la operación 6.")

    # ------------------------------------------------------------------
    # Operación 7: Reserva exitosa - confirmar y procesar.
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 7: Reserva exitosa - confirmar y procesar")
    try:
        reserva1 = Reserva(cliente=cliente1, servicio=sala, duracion=2, estado="PENDIENTE")
        reservas.append(reserva1)
        reserva1.mostrar_informacion()
        reserva1.confirmar()
        costo = reserva1.procesar(impuesto=0.19, descuento=0.10)
        print(f"Costo final procesado: ${costo:,.2f}")
    except SoftwareFJError as error:
        registrar_error(f"Operación 7 falló: {error}")
        print(f"Error controlado: {error}")
    else:
        registrar_evento("Operación 7 completada: reserva procesada correctamente.")
    finally:
        print("Fin de la operación 7.")

    # ------------------------------------------------------------------
    # Operación 8: Reserva fallida - duración inválida.
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 8: Reserva fallida - duración inválida")
    try:
        reserva_invalida = Reserva(cliente=cliente1, servicio=equipo, duracion=0)
        reservas.append(reserva_invalida)
    except (DatosInvalidosError, ParametroFaltanteError) as error:
        registrar_error(f"Operación 8: reserva inválida: {error}")
        print(f"Error controlado: {error}")
    finally:
        print("Fin de la operación 8.")

    # ------------------------------------------------------------------
    # Operación 9: Reserva fallida - operación no permitida y encadenamiento.
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 9: Reserva fallida - procesar sin confirmar (encadenamiento)")
    try:
        reserva2 = Reserva(cliente=cliente1, servicio=asesoria, duracion=3, estado="PENDIENTE")
        reservas.append(reserva2)
        try:
            # Se intenta procesar sin confirmar para provocar una operación no permitida.
            reserva2.procesar()
        except OperacionNoPermitidaError as error:
            # Encadenamiento de excepciones: se crea un error de reserva con causa original.
            raise ReservaInvalidaError(
                "La reserva no se puede procesar porque no fue confirmada."
            ) from error
    except ReservaInvalidaError as error:
        registrar_error(f"Operación 9: {error} | Causa: {error.__cause__}")
        print(f"Error controlado: {error}")
        print(f"Causa original: {error.__cause__}")
    finally:
        print("Fin de la operación 9.")

    # ------------------------------------------------------------------
    # Operación 10: Reserva exitosa con cancelación y manejo de estado.
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 10: Reserva confirmada y luego cancelada")
    try:
        # Se crea un segundo cliente válido para variar la simulación.
        cliente2 = Cliente("Luisa Martínez", "555666777", "luisa@correo.com")
        clientes.append(cliente2)
        reserva3 = Reserva(cliente=cliente2, servicio=equipo, duracion=2, estado="PENDIENTE")
        reservas.append(reserva3)
        reserva3.confirmar()
        reserva3.cancelar("El cliente cambió la fecha del alquiler.")
        print(f"Estado final de la reserva: {reserva3.estado}")
    except SoftwareFJError as error:
        registrar_error(f"Operación 10 falló: {error}")
        print(f"Error controlado: {error}")
    else:
        registrar_evento("Operación 10 completada: reserva cancelada correctamente.")
    finally:
        print("Fin de la operación 10.")

    # ------------------------------------------------------------------
    # Operación 11: Fallo por servicio no disponible (demuestra robustez).
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 11: Reserva de sala fallida - horario no disponible")
    try:
        inicio = datetime(2026, 11, 15, 8, 0)
        fin = datetime(2026, 11, 15, 10, 0)
        sala.registrar_reserva(inicio, fin, 10)
        # Esta segunda reserva se cruza con la primera y debe fallar.
        sala.registrar_reserva(
            datetime(2026, 11, 15, 9, 0),
            datetime(2026, 11, 15, 11, 0),
            8,
        )
    except ServicioNoDisponibleError as error:
        registrar_error(f"Operación 11: servicio no disponible: {error}")
        print(f"Error controlado: {error}")
    finally:
        print("Fin de la operación 11.")

    # ------------------------------------------------------------------
    # Operación 12: Cálculo inconsistente controlado (demostración adicional).
    # ------------------------------------------------------------------
    mostrar_titulo("Operación 12: Cálculo inválido controlado")
    try:
        # Se fuerza un dato inválido para demostrar validación de cálculo.
        asesoria.calcular_costo(impuesto=2, descuento=0, horas=1)
    except (DatosInvalidosError, CalculoInconsistenteError) as error:
        registrar_error(f"Operación 12: error de cálculo: {error}")
        print(f"Error controlado: {error}")
    else:
        print("Cálculo realizado correctamente.")
    finally:
        print("Fin de la operación 12.")

    # Resumen final para evidenciar que el sistema siguió funcionando.
    mostrar_titulo("Resumen final")
    print(f"Clientes registrados en memoria: {len(clientes)}")
    print(f"Servicios registrados en memoria: {len(servicios)}")
    print(f"Reservas registradas en memoria: {len(reservas)}")
    registrar_evento(
        f"Simulación finalizada. Clientes={len(clientes)}, Servicios={len(servicios)}, Reservas={len(reservas)}"
    )
    print("Simulación finalizada sin interrupciones.")


if __name__ == "__main__":
    # Punto de entrada principal del programa.
    try:
        main()
    except Exception as error:
        # Captura de último recurso: evita caída brusca y registra el error crítico.
        registrar_error(f"Error crítico no controlado: {error}",)
        print(f"Error crítico controlado: {error}")
    finally:
        print("Ejecución terminada.")
