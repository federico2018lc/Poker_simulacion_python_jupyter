# Simulación de manos de póker de 5 cartas

Este proyecto contiene una simulación reproducible de manos **independientes** de póker de cinco cartas. Genera manos aleatorias, las clasifica y compara la frecuencia observada de cada jugada.

## Alcance de esta versión

- Se usa un mazo estándar de 52 cartas, sin comodines.
- Cada observación es una mano de exactamente 5 cartas, sin cartas repetidas.
- Las manos son independientes entre sí: cada mano se extrae desde el mazo completo. Por eso, una carta puede aparecer en manos distintas.
- Se reconocen escalera real, escalera de color, póker, full house, color, escalera (incluida A-2-3-4-5), trío, doble pareja, pareja y carta alta.
- No se simulan cartas comunitarias, jugadores ni rondas de Texas Hold'em.

## Notebook

Abrí [poker_simulacion.ipynb](poker_simulacion.ipynb) y ejecutá todas las celdas desde el principio (`Run All`). El notebook usa únicamente la biblioteca estándar de Python, por lo que no requiere instalar dependencias.

La celda de parámetros concentra los valores que controlan el experimento:

```python
SEMILLA = 20260805
NUMERO_DE_MANOS = 100_000
```

Con la misma versión de Python y los mismos parámetros se obtienen las mismas manos y el mismo resumen. Para explorar otra muestra, cambiá `SEMILLA`; para mejorar la precisión de las frecuencias, aumentá `NUMERO_DE_MANOS`.

## Ejecución local

1. Instalá Python 3.10 o posterior.
2. Iniciá Jupyter Notebook o VS Code en esta carpeta.
3. Abrí el notebook y elegí un kernel de Python 3.
4. Usá `Run All` sin ejecutar celdas fuera de orden.

## Reproducibilidad y control de versiones

El notebook no escribe archivos ni depende de resultados de ejecuciones anteriores. Las celdas se guardan sin salidas para que el repositorio sólo versione código y explicaciones, no resultados transitorios.

Git registra los cambios locales en la rama actual. Cuando esta mejora esté verificada, el flujo habitual es: revisar el diff, crear un commit descriptivo, hacer push de la rama `rfc-001-notebook-reproducible` y abrir un pull request en GitHub.

