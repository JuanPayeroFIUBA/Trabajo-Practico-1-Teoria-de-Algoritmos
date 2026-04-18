"""
Trabajo Práctico 1 – Problema 3: BACKTRACKING
Teoría de Algoritmos – TB024 – UBA FIUBA
Curso Echevarría – 1er Cuatrimestre 2026
"""

import time
import sys
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIR_NAMES  = ['N', 'E', 'S', 'O']

sys.setrecursionlimit(500_000)
VERBOSE_MAX_CELLS = 200

# ─────────────────────────────────────────────────────────────────────────────
# SUPUESTOS
# 1. Grilla rectangular m×n: 'X'=pared, ' '=camino, 'E'=entrada, 'S'=salida.
# 2. Exactamente una 'E' y una 'S'. Posición fuera de grilla = pared.
# 3. Se prueban las 4 orientaciones iniciales.
# 4. DOS estructuras de control:
#    - visited_states (pos,dir): estados ya explorados en CUALQUIER rama.
#      Garantiza terminación — no se re-explora el mismo estado.
#    - path_set (pos): posiciones en el camino ACTIVO actual.
#      Garantiza camino simple — no se pisa una celda ya en el camino activo.
# 5. El backtrack es físico: la aspiradora vuelve a la celda anterior.
#    El camino final solo contiene las celdas del camino exitoso.
# 6. Complejidad temporal: O(m·n·4) = O(m·n). Espacial: O(m·n).
# ─────────────────────────────────────────────────────────────────────────────

def load_maze_from_file(filename):
    maze = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            if '\t' in line:
                row = [cell.strip().upper() or ' ' for cell in line.split('\t')]
            else:
                row = list(line)
            maze.append(row)
    if maze:
        max_cols = max(len(r) for r in maze)
        for row in maze:
            while len(row) < max_cols:
                row.append('X')
    return maze


def find_positions(maze):
    start = end = None
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            c = cell.upper()
            if c == 'E': start = (i, j)
            elif c == 'S': end = (i, j)
    return start, end


def look_ahead(maze, row, col, dir_idx):
    """Operación 1 – Ver adelante: PARED, CAMINO o SALIDA."""
    dr, dc = DIRECTIONS[dir_idx]
    nr, nc = row + dr, col + dc
    if not (0 <= nr < len(maze) and 0 <= nc < len(maze[0])):
        return 'PARED'
    cell = maze[nr][nc].upper()
    if cell == 'X':  return 'PARED'
    if cell == 'S':  return 'SALIDA'
    return 'CAMINO'


def turn_left(dir_idx):
    """Operación 3 – Girar 90° a la izquierda: N→O→S→E→N."""
    return (dir_idx + 3) % 4


# ─────────────────────────────────────────────────────────────────────────────
# BACKTRACKING
#
# PSEUDOCÓDIGO:
#   resolver(pos, dir, esAvance):
#     si (pos,dir) ∈ visitados → retornar FALSO
#     agregar (pos,dir) a visitados
#
#     si esAvance:
#       si pos ∈ caminoActivo → retornar FALSO   # no crear ciclos
#       si lab[pos] == SALIDA:
#         camino.append(pos); retornar VERDADERO
#       camino.append(pos); caminoActivo.add(pos)
#
#     adelante ← verAdelante(pos, dir)            # Op.1
#     si adelante ≠ PARED:
#       si resolver(avanzar(pos,dir), dir, True)  # Op.2
#         retornar VERDADERO
#
#     si resolver(pos, girarIzq(dir), False)      # Op.3
#       retornar VERDADERO
#
#     si esAvance:
#       camino.pop(); caminoActivo.remove(pos)    # BACKTRACK físico
#     retornar FALSO
# ─────────────────────────────────────────────────────────────────────────────

def solve(maze, visited_states, path, path_set, log,
          pos, dir_idx, is_advance, verbose, step):
    row, col = pos
    state = (row, col, dir_idx)

    if state in visited_states:
        return False
    visited_states.add(state)

    if is_advance:
        if pos in path_set:
            if verbose:
                log.append(f"           [descarta {pos}: ya está en el camino activo]")
            return False

        step[0] += 1

        if maze[row][col].upper() == 'S':
            path.append(pos)
            path_set.add(pos)
            if verbose:
                log.append(f"  Avance {step[0]:>4} │ prof={len(path):>3} │ {pos} dir={DIR_NAMES[dir_idx]} → SALIDA ✓")
            return True

        path.append(pos)
        path_set.add(pos)
        if verbose:
            log.append(f"  Avance {step[0]:>4} │ prof={len(path):>3} │ {pos} dir={DIR_NAMES[dir_idx]}")
    else:
        if verbose:
            log.append(f"           Gira → ahora mira {DIR_NAMES[dir_idx]}")

    # Operación 1
    ahead = look_ahead(maze, row, col, dir_idx)
    if verbose:
        log.append(f"           Ve adelante ({DIR_NAMES[dir_idx]}): {ahead}")

    # Operación 2: avanzar
    if ahead != 'PARED':
        dr, dc = DIRECTIONS[dir_idx]
        if solve(maze, visited_states, path, path_set, log,
                 (row + dr, col + dc), dir_idx, True, verbose, step):
            return True

    # Operación 3: girar izquierda
    new_dir = turn_left(dir_idx)
    if solve(maze, visited_states, path, path_set, log,
             pos, new_dir, False, verbose, step):
        return True

    # BACKTRACK físico: la aspiradora vuelve a la celda anterior
    if is_advance:
        path.pop()
        path_set.remove(pos)
        if verbose:
            parent = path[-1] if path else None
            log.append(f"  {'─'*9} BACKTRACK: abandona {pos}, vuelve físicamente a {parent} (prof={len(path)})")

    return False


def print_solution(maze, path_positions):
    display = [row[:] for row in maze]
    for (r, c) in path_positions:
        if display[r][c].upper() not in ('E', 'S'):
            display[r][c] = '.'
    for row in display:
        print('  ' + ''.join(row))


def run_maze(filename):
    maze = load_maze_from_file(filename)
    rows = len(maze)
    cols = len(maze[0]) if rows > 0 else 0
    total_cells = rows * cols

    start, end = find_positions(maze)
    if start is None:
        print(f"[{filename}] ERROR: no se encontró 'E'"); return None, rows, cols
    if end is None:
        print(f"[{filename}] ERROR: no se encontró 'S'"); return None, rows, cols

    verbose = (total_cells <= VERBOSE_MAX_CELLS)

    print(f"\n{'='*60}")
    print(f"Laberinto: {filename}  ({rows}×{cols})  [{total_cells} celdas]")
    print(f"Inicio: {start}   Salida: {end}")
    if verbose:
        print("Laberinto original:")
        for row in maze:
            print('  ' + ''.join(row))

    t0 = time.time()
    found = False
    path, log = [], []

    for initial_dir in range(4):
        visited_states = set()
        path, path_set, log = [], set(), []
        log.append(f"Orientación inicial: {DIR_NAMES[initial_dir]}")
        log.append(f"  {'─'*55}")
        step = [0]
        if solve(maze, visited_states, path, path_set, log,
                 start, initial_dir, True, verbose, step):
            found = True
            break

    elapsed = time.time() - t0

    if verbose:
        print(f"\n--- Seguimiento (Avance = movimiento físico real) ---")
        for line in log:
            print(line)

    print(f"\n--- Resultado ---")
    if found:
        print(f"Solución: {len(path)} celdas recorridas  ({elapsed:.6f} s)")
        if verbose:
            print("Camino final: " + " → ".join(str(p) for p in path))
            print("\nLaberinto con solución ('.' = camino):")
            print_solution(maze, path)
        return elapsed, rows, cols
    else:
        print(f"Sin solución  ({elapsed:.6f} s)")
        return None, rows, cols


def plot_times(labels, cell_counts, times, output_path="tiempos_backtracking.png"):
    if len(times) < 2:
        print("Se necesitan al menos 2 laberintos para graficar.")
        return
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(cell_counts, times, 'o-', color='steelblue',
            linewidth=2, markersize=8, label='Tiempo medido')
    scale   = max(times) / max(cell_counts)
    teorico = [n * scale for n in cell_counts]
    ax.plot(cell_counts, teorico, '--', color='tomato',
            linewidth=1.5, label='Curva teórica O(m·n) [escalada]')
    for n, t, lbl in zip(cell_counts, times, labels):
        ax.annotate(lbl, (n, t), textcoords="offset points",
                    xytext=(5, 4), fontsize=7, color='#333333')
    ax.set_xlabel("Tamaño del laberinto (celdas = m × n)", fontsize=11)
    ax.set_ylabel("Tiempo de ejecución (s)", fontsize=11)
    ax.set_title("Backtracking – Tiempo vs Tamaño\nComplejidad teórica: O(m·n)", fontsize=12)
    ax.legend(); ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout(); fig.savefig(output_path, dpi=150)
    print(f"\nGráfico guardado en: {output_path}")


def save_results(labels, cell_counts, times, output_path="resultados_backtracking.txt"):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("Resultados – Backtracking Laberinto\n" + "="*55 + "\n")
        f.write(f"{'Archivo':<30} {'Celdas':<15} {'Tiempo (s)'}\n" + "-"*55 + "\n")
        for lbl, nc, t in zip(labels, cell_counts, times):
            f.write(f"{lbl:<30} {nc:<15} {t:.6f}\n")
    print(f"Tabla guardada en: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python backtracking.py <archivo1.txt> [archivo2.txt ...]")
        sys.exit(1)

    labels, cell_counts, times = [], [], []

    for filepath in sys.argv[1:]:
        if not os.path.isfile(filepath):
            print(f"ADVERTENCIA: no se encontró '{filepath}', se omite.")
            continue
        elapsed, rows, cols = run_maze(filepath)
        if elapsed is not None:
            labels.append(os.path.basename(filepath))
            cell_counts.append(rows * cols)
            times.append(elapsed)

    if times:
        print(f"\n{'='*60}\nRESUMEN DE TIEMPOS\n{'='*60}")
        print(f"  {'Archivo':<28} {'Celdas':<10} {'Tiempo (s)'}")
        print("  " + "-"*50)
        for lbl, nc, t in zip(labels, cell_counts, times):
            print(f"  {lbl:<28} {nc:<10} {t:.6f}")
        save_results(labels, cell_counts, times)
        if len(times) > 1:
            plot_times(labels, cell_counts, times)
    else:
        print("\nNo se resolvió ningún laberinto correctamente.")