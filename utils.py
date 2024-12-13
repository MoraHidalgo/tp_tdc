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
def get_deviations(dias):
    deviations = []
    print("\nIngrese las desviaciones de temperatura.")
    print("Escriba 'done' para finalizar para usar un conjunto predefinido.\n")
    
    while True:
        time = input(f"Ingrese el tiempo de la desviación {len(deviations) + 1} (o 'done'/'otonio'): ").strip().lower()
        if time == 'done':
            break
        elif time == 'otonio': #Promedio de 10°C a las 00
            clima = [(60, 0), (120, 0), (180, 0), (240, 0), (300, 0), #10°C - 5h
                          (360, 0), (420, 0.0), (480, 1), (540, 1), (600, 2),#14°C - 10h
                          (660, 2), (720, 2), (780, 2), (840, 0), (900, 0),#20°C - 15h
                          (960, 0), (1020, 0), (1080, 0), (1140, -1), (1200, -1), #18°C - 20h
                          (1260, -2), (1320, -2), (1380, -2), (1440, -2)] #10°C - 0h
            
            for i in range(1,31): #Para que sea una semana
                deviations += [(item[0]*i, item[1]*0.01) for item in clima]
            break
        
        try:
            time = float(time)
            temperature = float(input(f"Ingrese la variación de temperatura {len(deviations) + 1}: "))
            deviations.append((time, temperature))
        except ValueError:
            print("Entrada inválida. Asegúrese de ingresar números válidos para el tiempo y la temperatura.")
    
    return deviations
