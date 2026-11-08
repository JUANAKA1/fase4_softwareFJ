import unittest
from abc import ABC

from excepciones.errores_personalizados import (
    DatosInvalidosError,
    ParametroFaltanteError,
)
from modelos.cliente import Cliente
from modelos.entidad import Entidad
from modelos.servicio import Servicio


class ServicioPrueba(Servicio):
    def calcular_costo(self, impuesto=0, descuento=0):
        return 100 * (1 + impuesto) * (1 - descuento)

    def describir(self):
        return "Servicio de prueba"

    def validar_parametros(self):
        return True


class ComponentesIntegranteUnoTests(unittest.TestCase):
    def test_entidad_y_servicio_son_abstractos(self):
        self.assertTrue(issubclass(Entidad, ABC))
        with self.assertRaises(TypeError):
            Servicio()

    def test_servicio_concreto_cumple_el_contrato(self):
        servicio = ServicioPrueba()
        self.assertAlmostEqual(servicio.calcular_costo(0.19, 0.1), 107.1)
        self.assertEqual(servicio.mostrar_informacion(), "Servicio de prueba")

    def test_cliente_normaliza_y_encapsula_datos(self):
        cliente = Cliente("  Ana   Pérez ", " 00123 ", "ANA@EJEMPLO.COM")

        self.assertEqual(cliente.nombre, "Ana Pérez")
        self.assertEqual(cliente.identificacion, "00123")
        self.assertEqual(cliente.correo, "ana@ejemplo.com")
        self.assertFalse(hasattr(cliente, "__nombre"))

    def test_cliente_rechaza_datos_invalidos_y_faltantes(self):
        with self.assertRaises(ParametroFaltanteError):
            Cliente()
        with self.assertRaises(DatosInvalidosError):
            Cliente("Ana", "123", "correo-invalido")
        with self.assertRaises(DatosInvalidosError):
            Cliente("Ana", "", "ana@ejemplo.com")

    def test_error_de_validacion_se_registra(self):
        from utilidades.logger import logger

        with self.assertLogs(logger, level="ERROR"):
            with self.assertRaises(DatosInvalidosError):
                Cliente("Ana", "123", "correo-invalido")


if __name__ == "__main__":
    unittest.main()
