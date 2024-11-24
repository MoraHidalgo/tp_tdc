def get_double(prompt, min, max):
    while True:
        try:
            value = float(input(prompt))
            if min <= value <= max:
                return value
            print(f"Por favor, ingrese un número entre {min} y {max}.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

# Función para obtener una lista de tuplas de desviaciones del usuario
def get_deviations():
    deviations = []
    print("\nIngrese las desviaciones de temperatura. Cada desviación consta de:")
    print("  - Tiempo (en minutos)")
    print("  - Variación de temperatura (en °C)")
    print("Escriba 'done' para finalizar o 'default' para usar un conjunto predefinido.\n")
    
    while True:
        time = input(f"Ingrese el tiempo de la desviación {len(deviations) + 1} (o 'done'/'default'): ").strip().lower()
        if time == 'done':
            break
        elif time == 'default':
            deviations = [(100, 0.1), (200, -0.1)]
            print(f"Se usará el conjunto predefinido: {deviations}")
            break
        
        try:
            time = float(time)
            temperature = float(input(f"Ingrese la variación de temperatura {len(deviations) + 1}: "))
            deviations.append((time, temperature))
        except ValueError:
            print("Entrada inválida. Asegúrese de ingresar números válidos para el tiempo y la temperatura.")
    
    return deviations
