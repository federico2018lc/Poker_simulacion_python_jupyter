import itertools
import unittest
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from poker_sim import Card, Categoria, evaluar_mano, mazo_estandar


def cartas(texto):
    rangos = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
    return [
        Card(rangos[item[0]] if item[0] in rangos else int(item[0]), item[1])
        for item in texto.split()
    ]


class EvaluadorManosConocidasTest(unittest.TestCase):
    def test_categorias_conocidas(self):
        casos = {
            "A♠ K♠ Q♠ J♠ T♠": Categoria.ESCALERA_REAL,
            "9♥ 8♥ 7♥ 6♥ 5♥": Categoria.ESCALERA_DE_COLOR,
            "A♠ A♥ A♦ A♣ K♠": Categoria.POKER,
            "Q♠ Q♥ Q♦ 2♣ 2♦": Categoria.FULL_HOUSE,
            "A♣ J♣ 8♣ 4♣ 2♣": Categoria.COLOR,
            "A♠ 2♥ 3♦ 4♣ 5♠": Categoria.ESCALERA,
            "7♠ 7♥ 7♦ K♣ 2♠": Categoria.TRIO,
            "J♠ J♥ 4♦ 4♣ A♠": Categoria.DOBLE_PAREJA,
            "9♠ 9♥ A♦ 7♣ 2♠": Categoria.PAREJA,
            "A♠ J♥ 8♦ 4♣ 2♠": Categoria.CARTA_ALTA,
        }
        for mano, categoria in casos.items():
            with self.subTest(mano=mano):
                self.assertEqual(evaluar_mano(cartas(mano)).categoria, categoria)

    def test_desempates(self):
        pareja_de_ases = evaluar_mano(cartas("A♠ A♥ K♦ 7♣ 2♠"))
        pareja_de_reyes = evaluar_mano(cartas("K♠ K♥ Q♦ J♣ 9♠"))
        escalera_alta = evaluar_mano(cartas("9♠ T♥ J♦ Q♣ K♠"))
        escalera_baja = evaluar_mano(cartas("A♠ 2♥ 3♦ 4♣ 5♠"))
        self.assertGreater(pareja_de_ases.score, pareja_de_reyes.score)
        self.assertGreater(escalera_alta.score, escalera_baja.score)

    def test_manos_invalidas(self):
        with self.assertRaises(ValueError):
            evaluar_mano(cartas("A♠ K♥ Q♦ J♣"))
        with self.assertRaises(ValueError):
            evaluar_mano(cartas("A♠ A♠ Q♦ J♣ T♠"))


class ValidacionExhaustivaTest(unittest.TestCase):
    def test_las_2598960_manos_tienen_los_conteos_teoricos(self):
        conteos = Counter(
            evaluar_mano(mano).categoria
            for mano in itertools.combinations(mazo_estandar(), 5)
        )
        esperados = {
            Categoria.ESCALERA_REAL: 4,
            Categoria.ESCALERA_DE_COLOR: 36,
            Categoria.POKER: 624,
            Categoria.FULL_HOUSE: 3744,
            Categoria.COLOR: 5108,
            Categoria.ESCALERA: 10200,
            Categoria.TRIO: 54912,
            Categoria.DOBLE_PAREJA: 123552,
            Categoria.PAREJA: 1098240,
            Categoria.CARTA_ALTA: 1302540,
        }
        self.assertEqual(conteos, esperados)
        self.assertEqual(sum(conteos.values()), 2598960)
