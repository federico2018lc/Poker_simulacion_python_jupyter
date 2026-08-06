"""Modelo y evaluación de manos de póker de cinco cartas."""

from .evaluator import (
    CATEGORIAS_EN_ORDEN,
    CONTEOS_TEORICOS,
    Card,
    Categoria,
    EstadisticaCategoria,
    EvaluacionMano,
    TOTAL_MANOS_POSIBLES,
    evaluar_mano,
    mazo_estandar,
    resumir_estadisticas,
)

__all__ = [
    "CATEGORIAS_EN_ORDEN",
    "CONTEOS_TEORICOS",
    "Card",
    "Categoria",
    "EstadisticaCategoria",
    "EvaluacionMano",
    "TOTAL_MANOS_POSIBLES",
    "evaluar_mano",
    "mazo_estandar",
    "resumir_estadisticas",
]
