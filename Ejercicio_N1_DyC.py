def encontrar_moneda_mas_liviana_dyc(monedas):
    cantidad = len(monedas)
    if cantidad == 1:
        return 0

    mitad = cantidad // 2
    if cantidad % 2 != 0:
        mitad_izquierda = monedas[:mitad]
        mitad_derecha = monedas[mitad + 1 :]
        if pesar_grupos_de_monedas(mitad_izquierda, mitad_derecha) == 0:
            return mitad
        mitad += 1
    else:
        mitad_izquierda = monedas[:mitad]
        mitad_derecha = monedas[mitad:]

    if pesar_grupos_de_monedas(mitad_izquierda, mitad_derecha) < 0:
        return encontrar_moneda_mas_liviana_dyc(mitad_izquierda)
    return mitad + encontrar_moneda_mas_liviana_dyc(mitad_derecha)


def pesar_grupos_de_monedas(grupo1, grupo2):
    return sum(grupo1) - sum(grupo2)


def main():
    # en el enunciado no especifica que se conozcan los pesos de las monedas, por lo que se asume que se tiene una lista con los pesos de cada moneda de modo que todas tienen un peso estandar (1 en este caso) excepto una que es la que hay que buscar
    # si no fuera el caso, se implementaria un for que recorra todas las monedas y obtenga su peso  luego lo guarde en una lista para ejecutar la funcion que encuentre la moneda mas liviana, lo cual seria O(n) y no sumaria a la complejidad de la funcion porque esta ya es O(n)
    monedas_pesos = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1]

    moneda_mas_liviana = encontrar_moneda_mas_liviana_dyc(monedas_pesos)
    print(
        f"La moneda más liviana de las {len(monedas_pesos)} que hay es la {moneda_mas_liviana + 1}°"
    )


main()
