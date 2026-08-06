"""Reglas de evaluación para manos independientes de póker de cinco cartas."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from itertools import product
from typing import Iterable


RANGOS = tuple(range(2, 15))
PALOS = ("♠", "♥", "♦", "♣")
NOMBRES_RANGO = {11: "J", 12: "Q", 13: "K", 14: "A"}


@dataclass(frozen=True, order=True)
class Card:
    """Carta inmutable con rango explícito (2..14) y palo."""

    rango: int
    palo: str

    def __post_init__(self) -> None:
        if self.rango not in RANGOS:
            raise ValueError("El rango debe estar entre 2 y 14.")
        if self.palo not in PALOS:
            raise ValueError(f"Palo no válido: {self.palo!r}")

    def __str__(self) -> str:
        return f"{NOMBRES_RANGO.get(self.rango, self.rango)}{self.palo}"


class Categoria(IntEnum):
    CARTA_ALTA = 0
    PAREJA = 1
    DOBLE_PAREJA = 2
    TRIO = 3
    ESCALERA = 4
    COLOR = 5
    FULL_HOUSE = 6
    POKER = 7
    ESCALERA_DE_COLOR = 8
    ESCALERA_REAL = 9


CATEGORIAS_EN_ORDEN = tuple(reversed(tuple(Categoria)))
NOMBRES_CATEGORIA = {
    Categoria.CARTA_ALTA: "Carta alta",
    Categoria.PAREJA: "Pareja",
    Categoria.DOBLE_PAREJA: "Doble pareja",
    Categoria.TRIO: "Trío",
    Categoria.ESCALERA: "Escalera",
    Categoria.COLOR: "Color",
    Categoria.FULL_HOUSE: "Full house",
    Categoria.POKER: "Póker",
    Categoria.ESCALERA_DE_COLOR: "Escalera de color",
    Categoria.ESCALERA_REAL: "Escalera real",
}


@dataclass(frozen=True)
class EvaluacionMano:
    """Resultado comparable; el mayor score gana."""

    categoria: Categoria
    desempate: tuple[int, ...]

    @property
    def score(self) -> tuple[Categoria, tuple[int, ...]]:
        return self.categoria, self.desempate

    @property
    def nombre(self) -> str:
        return NOMBRES_CATEGORIA[self.categoria]


def mazo_estandar() -> tuple[Card, ...]:
    return tuple(Card(rango, palo) for rango, palo in product(RANGOS, PALOS))


def _alto_escalera(rangos: Iterable[int]) -> int | None:
    unicos = sorted(set(rangos))
    if len(unicos) != 5:
        return None
    if unicos == [2, 3, 4, 5, 14]:
        return 5
    if unicos[-1] - unicos[0] == 4:
        return unicos[-1]
    return None


def evaluar_mano(mano: Iterable[Card]) -> EvaluacionMano:
    """Evalúa exactamente cinco cartas distintas y devuelve su fuerza."""

    cartas = tuple(mano)
    if len(cartas) != 5:
        raise ValueError("Una mano debe contener exactamente cinco cartas.")
    if len(set(cartas)) != 5:
        raise ValueError("Una mano no puede contener cartas repetidas.")

    rangos = [carta.rango for carta in cartas]
    palos = [carta.palo for carta in cartas]
    conteos = Counter(rangos)
    grupos = sorted(
        ((cantidad, rango) for rango, cantidad in conteos.items()),
        reverse=True,
    )
    es_color = len(set(palos)) == 1
    alto_escalera = _alto_escalera(rangos)

    if es_color and alto_escalera == 14:
        return EvaluacionMano(Categoria.ESCALERA_REAL, (14,))
    if es_color and alto_escalera is not None:
        return EvaluacionMano(Categoria.ESCALERA_DE_COLOR, (alto_escalera,))
    if grupos[0][0] == 4:
        poker = grupos[0][1]
        restante = grupos[1][1]
        return EvaluacionMano(Categoria.POKER, (poker, restante))
    if [cantidad for cantidad, _ in grupos] == [3, 2]:
        return EvaluacionMano(Categoria.FULL_HOUSE, (grupos[0][1], grupos[1][1]))
    if es_color:
        return EvaluacionMano(Categoria.COLOR, tuple(sorted(rangos, reverse=True)))
    if alto_escalera is not None:
        return EvaluacionMano(Categoria.ESCALERA, (alto_escalera,))
    if grupos[0][0] == 3:
        trio = grupos[0][1]
        restantes = sorted((rango for rango in rangos if rango != trio), reverse=True)
        return EvaluacionMano(Categoria.TRIO, (trio, *restantes))
    if [cantidad for cantidad, _ in grupos] == [2, 2, 1]:
        parejas = sorted((rango for cantidad, rango in grupos if cantidad == 2), reverse=True)
        restante = next(rango for cantidad, rango in grupos if cantidad == 1)
        return EvaluacionMano(Categoria.DOBLE_PAREJA, (*parejas, restante))
    if grupos[0][0] == 2:
        pareja = grupos[0][1]
        restantes = sorted((rango for rango in rangos if rango != pareja), reverse=True)
        return EvaluacionMano(Categoria.PAREJA, (pareja, *restantes))
    return EvaluacionMano(Categoria.CARTA_ALTA, tuple(sorted(rangos, reverse=True)))
