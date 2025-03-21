import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración del tablero
TAMANO_CUADRO = 80
FILAS = 8
COLUMNAS = 8
ANCHO = ALTO = TAMANO_CUADRO * FILAS

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Crear la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Problema de las 8 Reinas")

# Función para dibujar el tablero
def dibujar_tablero(tablero):
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            color = ROJO if (fila + columna) % 2 == 0 else NEGRO
            pygame.draw.rect(ventana, color, (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
            if tablero[fila][columna] == 1:
                pygame.draw.circle(ventana, BLANCO, (columna * TAMANO_CUADRO + TAMANO_CUADRO // 2, fila * TAMANO_CUADRO + TAMANO_CUADRO // 2), TAMANO_CUADRO // 3)

# Función para rotar el tablero 90 grados
def rotar_tablero(tablero):
    return [list(fila) for fila in zip(*tablero[::-1])]

# Función para reflejar el tablero horizontalmente
def reflejar_tablero(tablero):
    return [fila[::-1] for fila in tablero]

# Generar las 92 soluciones únicas
def generar_soluciones():
    soluciones = []

    def es_seguro(tablero, fila, columna):
        for i in range(columna):
            if tablero[fila][i] == 1:
                return False
        i, j = fila, columna
        while i >= 0 and j >= 0:
            if tablero[i][j] == 1:
                return False
            i -= 1
            j -= 1
        i, j = fila, columna
        while i < FILAS and j >= 0:
            if tablero[i][j] == 1:
                return False
            i += 1
            j -= 1
        return True

    def resolver(tablero, columna):
        if columna >= COLUMNAS:
            soluciones.append([fila[:] for fila in tablero])
            return
        for fila in range(FILAS):
            if es_seguro(tablero, fila, columna):
                tablero[fila][columna] = 1
                resolver(tablero, columna + 1)
                tablero[fila][columna] = 0

    tablero_vacio = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
    resolver(tablero_vacio, 0)
    return soluciones

# Cargar las 92 soluciones únicas
soluciones_unicas = generar_soluciones()

# Función para encontrar una solución que incluya la posición seleccionada
def encontrar_solucion(fila, columna):
    for solucion in soluciones_unicas:
        if solucion[fila][columna] == 1:
            return solucion
    return None

# Función principal
def main():
    tablero = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                pygame.quit()
                sys.exit()

            # Seleccionar la posición de la primera reina con el mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                fila = y // TAMANO_CUADRO
                columna = x // TAMANO_CUADRO
                if 0 <= fila < FILAS and 0 <= columna < COLUMNAS:
                    solucion = encontrar_solucion(fila, columna)
                    if solucion:
                        tablero = solucion
                        print("Solución encontrada:")
                        for fila in tablero:
                            print(fila)
                    else:
                        print("No se encontró solución para esta posición.")

        ventana.fill(BLANCO)
        dibujar_tablero(tablero)
        pygame.display.flip()

# Ejecutar el programa
if __name__ == "__main__":
    main()