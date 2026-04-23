# Trabajo Práctico 1 — Teoría de Algoritmos (TB024)
Curso Echevarría — 1er Cuatrimestre 2026

## Configuración del entorno

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Problema 1 — División y Conquista

**Archivo:** `Problema_1/Ejercicio_N1_DyC.py`

Encuentra la moneda falsa (la más liviana) dentro de una bolsa de `n` monedas usando División y Conquista. Divide el conjunto en dos mitades, pesa ambos grupos y descarta recursivamente la mitad más pesada.

Los pesos de las monedas están definidos directamente en el código como una lista (todas con peso `1` excepto la falsa con peso `0.5`).

```bash
python Problema_1/Ejercicio_N1_DyC.py
```

---

## Problema 2 — Greedy (Dijkstra)

**Archivo:** `Problema_2/greedy.py`

Traducción a Python del archivo `paolo.bas`. Implementa el algoritmo de Dijkstra para encontrar el camino mínimo desde un vértice de origen hacia todos los demás vértices de un grafo no dirigido con pesos.

El programa es interactivo: pide el número de vértices, los ejes con sus costos (ingresar `0,0` para terminar) y el vértice de salida.

```bash
python Problema_2/greedy.py
```

Datos de prueba del enunciado (11 vértices):
```
Eje 1,2 → costo 66
Eje 2,3 → costo 122
Eje 2,4 → costo 126
Eje 3,4 → costo 80
Eje 3,5 → costo 148
Eje 4,5 → costo 126
Eje 5,6 → costo 49
Eje 6,7 → costo 101
Eje 7,8 → costo 69
Eje 7,9 → costo 72
Eje 8,9 → costo 45
Eje 8,11 → costo 56
Eje 11,10 → costo 30
Eje 10,9 → costo 46
```

---

## Problema 3 — Backtracking (Laberinto)

**Archivo:** `Problema_3/backtracking.py`

Resuelve laberintos rectangulares codificados en archivos `.txt` usando backtracking. La aspiradora solo puede ver adelante, avanzar o girar 90° a la izquierda.

- `X` = pared, espacio en blanco = camino, `E` = entrada, `S` = salida
- Para laberintos de hasta 200 celdas muestra el seguimiento paso a paso
- Genera automáticamente `resultados_backtracking.txt` y `tiempos_backtracking.png` si se pasan múltiples archivos

```bash
# Un laberinto
python Problema_3/backtracking.py Problema_3/ej1.txt

# Múltiples laberintos (genera gráfico comparativo)
python Problema_3/backtracking.py Problema_3/ej1.txt Problema_3/ej2.txt Problema_3/ej3.txt
python Problema_3/backtracking.py Problema_3/5x5.txt Problema_3/10x10.txt Problema_3/20x20.txt
```

**Sets de datos incluidos:**

| Archivo   | Tamaño  |
|-----------|---------|
| `ej1.txt` | 7×6     |
| `ej2.txt` | 8×10    |
| `ej3.txt` | 12×15   |
| `5x5.txt` | 5×5     |
| `10x10.txt` | 10×10 |
| `20x20.txt` | 20×20 |

---

## Problema 4 — Programación Dinámica (Palíndromos)

**Archivo:** `Problema_4/pd.py`

Encuentra el mínimo número de palíndromos en que se puede descomponer una cadena usando programación dinámica con memoización. Genera cadenas aleatorias con semilla fija (`random.seed(42)`) para reproducibilidad, mide los tiempos de ejecución y muestra un gráfico comparando los tiempos medidos con la curva teórica O(n²).

```bash
python Problema_4/pd.py
```
