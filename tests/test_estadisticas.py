import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from poker_sim import (
    CATEGORIAS_EN_ORDEN,
    CONTEOS_TEORICOS,
    Card,
    Categoria,
    TOTAL_MANOS_POSIBLES,
    evaluar_mano,
    resumir_estadisticas,
)


class EstadisticasTest(unittest.TestCase):
    def test_los_conteos_teoricos_suman_todas_las_manos(self):
        self.assertEqual(sum(CONTEOS_TEORICOS.values()), TOTAL_MANOS_POSIBLES)

    def test_el_resumen_incluye_categorias_ausentes(self):
        mano = [
            Card(14, "♠"),
            Card(14, "♥"),
            Card(13, "♦"),
            Card(7, "♣"),
            Card(2, "♠"),
        ]
        filas = resumir_estadisticas([evaluar_mano(mano)])
        por_categoria = {fila.categoria: fila for fila in filas}

        self.assertEqual(len(filas), len(CATEGORIAS_EN_ORDEN))
        self.assertEqual(por_categoria[Categoria.PAREJA].observadas, 1)
        self.assertEqual(por_categoria[Categoria.POKER].observadas, 0)
        self.assertEqual(por_categoria[Categoria.PAREJA].total_muestra, 1)
        self.assertAlmostEqual(
            por_categoria[Categoria.PAREJA].porcentaje_observado,
            1.0,
        )

    def test_no_acepta_una_muestra_vacia(self):
        with self.assertRaises(ValueError):
            resumir_estadisticas([])
