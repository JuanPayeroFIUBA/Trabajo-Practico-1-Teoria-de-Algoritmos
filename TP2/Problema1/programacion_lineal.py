import pulp

# Constantes Pi: Paradas solicitadas por cliente
PARADAS_POR_CLIENTE = {
    "Cliente_A": 30,
    "Cliente_B_Op1": 80,
    "Cliente_B_Op2": 120,
    "Cliente_C": 75,
    "Cliente_D": 50,
    "Cliente_E": 2,
    "Cliente_F": 20,
    "Cliente_G": 100,
}

# Constantes Oi: Oferta economica de cada cliente
BENEFICIO_POR_CLIENTE = {
    "Cliente_A": 50000,
    "Cliente_B_Op1": 100000,
    "Cliente_B_Op2": 120000,
    "Cliente_C": 100000,
    "Cliente_D": 80000,
    "Cliente_E": 5000,
    "Cliente_F": 40000,
    "Cliente_G": 90000,
}

CAPACIDAD_MAXIMA_PARADAS = 200


def resolver_pl():
    # 1. Declarar el problema de maximización
    prob = pulp.LpProblem("Maximizacion_Concesiones", pulp.LpMaximize)
    clientes = list(PARADAS_POR_CLIENTE.keys())

    # 2. Instanciación dinámica de las variables binarias Yi
    Y = pulp.LpVariable.dicts("Y", clientes, cat="Binary")

    # 3. Función Objetivo: Sumatoria(Oi * Yi)
    prob += (
        pulp.lpSum([BENEFICIO_POR_CLIENTE[c] * Y[c] for c in clientes]),
        "Ingreso_Total",
    )

    # 4. Restricción Límite de Infraestructura: Sumatoria(Pi * Yi) <= 200
    prob += (
        pulp.lpSum([PARADAS_POR_CLIENTE[c] * Y[c] for c in clientes])
        <= CAPACIDAD_MAXIMA_PARADAS,
        "Max_Paradas",
    )

    # 5. Restricciones Lógicas
    prob += Y["Cliente_B_Op1"] + Y["Cliente_B_Op2"] <= 1, "Excluyente_ClienteB"
    prob += Y["Cliente_A"] + Y["Cliente_D"] <= 1, "Excluyente_Competidores_AyD"

    # 6. Resolución algorítmica por Branch & Bound
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # 7. Guardado del reporte en TXT
    with open("pl_resultado.txt", "w") as f:
        f.write(f"Estado de la resolucion: {pulp.LpStatus[prob.status]}\n")
        f.write(f"Ingreso Optimo Total: USD {pulp.value(prob.objective)}\n\n")
        f.write("Plan de Concesiones Aprobado:\n")

        paradas_usadas = 0
        for c in clientes:
            if Y[c].varValue == 1.0:
                f.write(
                    f"- {c} (Usa {PARADAS_POR_CLIENTE[c]} paradas | Ingreso USD {BENEFICIO_POR_CLIENTE[c]})\n"
                )
                paradas_usadas += PARADAS_POR_CLIENTE[c]

        f.write(
            f"\nUso de infraestructura: {paradas_usadas} de {CAPACIDAD_MAXIMA_PARADAS} paradas disponibles.\n"
        )

    print("Modelo resuelto con éxito. Reporte guardado en 'pl_resultados.txt'.")


if __name__ == "__main__":
    resolver_pl()
