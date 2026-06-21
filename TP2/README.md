# Trabajo Práctico N°2 — Teoría de Algoritmos

**Grupo N° 4**

- Tania Friedenberger (108823)
- Marco Tosi (107237)
- Juan Ignacio Payero (113195)
- Julieta Bloise (98592)
- Guillermo Hahn (112761)

---

## Requisitos

- **Lenguaje:** Python 3
- **Versión mínima:** Python 3.8 o superior
- **Sistema operativo:** Multiplataforma (Linux, macOS, Windows)

### Bibliotecas requeridas

- `pulp` — modelado y resolución de Programación Lineal Entera (Problema 1)
- `matplotlib` — generación de gráficos (Problemas 2 y 3)

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install pulp matplotlib
```

---

## Estructura del proyecto

```
.
├── Informe_tp1_grupo4.pdf          # Documento con carátula, índice, pseudocódigos, demostraciones e informes
├── Problema1/
│   ├── programacion_lineal.py      # Script principal
│   ├── pl_resultado.txt            # Resultado de la ejecución
│   └── pl_readme.md                # Instrucciones específicas del Problema 1
├── Problema2/
│   ├── resolucionPunto2.py         # Script principal (redes de flujo + Edmonds-Karp)
│   ├── clasesFlujo.py              # Implementación de Edmonds-Karp
│   ├── generadorDeDatasets.py      # Lectura de datasets
│   ├── datasets/                   # 6 sets de datos de entrada
│   │   ├── d1.txt ... d6.txt
│   └── resultados/                 # Generado automáticamente al ejecutar
│       ├── resultado_d1.txt ... resultado_d6.txt
│       └── tiempos_problema2.png
├── Problema3/
│   ├── problema3.py                # Script principal (algoritmo de aproximación)
│   ├── informe_problema3.md        # Informe detallado en Markdown
│   ├── datasets/                   # 9 sets de datos generados con semilla fija
│   │   ├── dataset_n100.txt ... dataset_n100000.txt
│   └── results/                    # Generado automáticamente al ejecutar
│       ├── tiempos.csv
│       └── tiempos_problema3.png
└── Problema4/
    ├── ejercicio_RA.py             # Script principal (3-coloreo aleatorio)
    ├── grafo.py                    # Clase Grafo (listas de adyacencia)
    ├── sets_datos.py               # Carga de grafos desde archivos
    ├── datasets/                   # 4 sets de datos de entrada
    │   ├── dataset1.txt ... dataset4.txt
    └── resultados_datasets/        # Resultados de ejecución previos
        ├── resultado_dataset1.txt ... resultados_dataset4.txt
```

---

## Instrucciones de ejecución

### Problema 1 — Programación Lineal

Desde la carpeta `Problema1/`:

```bash
cd Problema1
python3 programacion_lineal.py
```

**Salida:** se crea/actualiza el archivo `pl_resultado.txt` con la solución óptima.

---

### Problema 2 — Redes de Flujo

Desde la carpeta `Problema2/` (o desde cualquier otra ruta):

```bash
cd Problema2
python3 resolucionPunto2.py
```

**Salida:**
- En consola: tiempos de ejecución por dataset.
- En la carpeta `resultados/`: un archivo `resultado_dX.txt` por cada dataset procesado.
- En la carpeta `resultados/`: gráfico `tiempos_problema2.png` comparando tiempos reales vs. curva teórica.

---

### Problema 3 — Algoritmos de Aproximación

Desde la carpeta `Problema3/` (o desde cualquier otra ruta):

```bash
cd Problema3
python3 problema3.py
```

**Salida:**
- En consola: tabla de seguimiento con instancias pequeñas y resultados de experimentos.
- En la carpeta `results/`: archivo `tiempos.csv` y gráfico `tiempos_problema3.png`.

> Nota: si el archivo `results/tiempos.csv` ya existe, el script reutiliza los tiempos guardados. Borrarlo para volver a medir.

---

### Problema 4 — Algoritmos Aleatorios

Desde la carpeta `Problema4/` (o desde cualquier otra ruta):

```bash
cd Problema4
python3 ejercicio_RA.py
```

**Salida:**
- En consola: satisfacción de una ejecución individual, promedio de 10.000 iteraciones y valor teórico esperado.

> Nota: por defecto el script utiliza `dataset4.txt`. Para probar otros datasets se recomienda importar la función `tres_coloreo_randomizado` desde otro script o modificar la ruta en `main()`.

---

## Notas adicionales

- Los scripts utilizan rutas relativas al archivo `.py`, por lo que pueden ejecutarse desde cualquier directorio de trabajo.
- Los datasets del Problema 3 se generan automáticamente con una **semilla fija** (`seed = 2024 + n`) para garantizar reproducibilidad.
- Los resultados previos del Problema 4 se encuentran en `Problema4/resultados_datasets/`.
