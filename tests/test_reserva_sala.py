
import unittest
from datetime import datetime

from modelos.reserva_sala import ReservaSala
from excepciones.errores_personalizados import (
    DatosInvalidosError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)


class ReservaSalaTests(unittest.TestCase):

    def setUp(self):
        self.sala = ReservaSala(
            nombre_sala="Sala Principal",
            capacidad=20,
            precio_hora=50000
        )

    def test_crear_sala_correctamente(self):
        self.assertEqual(self.sala.nombre_sala, "Sala Principal")
        self.assertEqual(self.sala.capacidad, 20)
        self.assertEqual(self.sala.precio_hora, 50000)

    def test_calcular_costo(self):
        costo = self.sala.calcular_costo(duracion_horas=2)
        self.assertEqual(costo, 100000)

    def test_rechazar_cantidad_superior_a_capacidad(self):
        with self.assertRaises(ReservaInvalidaError):
            self.sala.validar_capacidad(25)

    def test_rechazar_duracion_invalida(self):
        with self.assertRaises(DatosInvalidosError):
            self.sala.calcular_costo(duracion_horas=0)

    def test_rechazar_reserva_con_fecha_invalida(self):
        with self.assertRaises(ReservaInvalidaError):
            self.sala.verificar_disponibilidad(
                datetime(2026, 11, 15, 12, 0),
                datetime(2026, 11, 15, 10, 0)
            )

    def test_rechazar_reservas_que_se_cruzan(self):
        inicio = datetime(2026, 11, 15, 8, 0)
        fin = datetime(2026, 11, 15, 10, 0)

        self.sala.registrar_reserva(inicio, fin, 10)

        with self.assertRaises(ServicioNoDisponibleError):
            self.sala.registrar_reserva(
                datetime(2026, 11, 15, 9, 0),
                datetime(2026, 11, 15, 11, 0),
                8
            )


if __name__ == "__main__":
    unittest.main()

