import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_double, get_deviations

# Parámetros de simulación
time_step = 1  # Paso de tiempo en minutos
total_time = 2880  # Tiempo total de simulación (48 horas)

# Parámetros del agua
set_point = get_double("Ingrese la temperatura deseada del agua (°C): ", 20, 35)
initial_temperature = get_double("Ingrese la temperatura inicial del agua (°C): ", 10, 30)

# Dinámica del climatizador
max_heating_rate = 0.5  # Grados Celsius por minuto
max_cooling_rate = -0.5  # Grados Celsius por minuto
heat_transfer_coefficient = 0.01  # Eficiencia térmica del climatizador

# Controlador PID
Kp = 0.3
Ki = 0.02
Kd = 0.01

# Inicialización
temperature = initial_temperature
integral = 0
previous_error = set_point - temperature
temperatures = [temperature]
times = [0]
heater_power = [0]  # Potencia de calentamiento/enfriamiento normalizada

# Simulación
for t in range(1, total_time + 1):
    error = set_point - temperature
    integral += error * time_step
    derivative = (error - previous_error) / time_step

    # Salida PID
    control_signal = Kp * error + Ki * integral + Kd * derivative

    # Limitar la señal de control según las capacidades del climatizador
    control_signal = max(min(control_signal, max_heating_rate), max_cooling_rate)

    # Anti-reset windup
    if control_signal == max_heating_rate or control_signal == max_cooling_rate:
        integral -= error * time_step

    # Modelo de transferencia de calor
    temperature += heat_transfer_coefficient * control_signal * time_step
    temperatures.append(temperature)
    times.append(t)
    heater_power.append(control_signal / max_heating_rate if control_signal > 0 else control_signal / max_cooling_rate)

    previous_error = error

# Creación del DataFrame
data = pd.DataFrame({
    'Tiempo (min)': times,
    'Temperatura del agua (°C)': temperatures,
    'Potencia del climatizador': heater_power
})

# Gráficos
plt.figure(figsize=(10, 6))

# Temperatura del agua
plt.plot(data['Tiempo (min)'], data['Temperatura del agua (°C)'], label='Temperatura del agua')
plt.axhline(y=set_point, color='r', linestyle='--', label='Temperatura deseada')
plt.xlabel('Tiempo (min)')
plt.ylabel('Temperatura (°C)')
plt.title('Simulación de Control de Temperatura de una Piscina')
plt.legend()
plt.grid(True)

# Potencia del climatizador
plt.figure(figsize=(10, 3))
plt.plot(data['Tiempo (min)'], data['Potencia del climatizador'], label='Potencia del climatizador')
plt.xlabel('Tiempo (min)')
plt.ylabel('Potencia (normalizada)')
plt.title('Potencia del climatizador')
plt.legend()
plt.grid(True)

plt.show()

# Resumen
print("Temperatura final del agua: {:.2f} °C".format(temperatures[-1]))
print("Tiempo total de simulación: {} minutos".format(total_time))
print("Temperatura deseada: {} °C".format(set_point))
print("\nResumen de los datos:")
print(data.describe())
