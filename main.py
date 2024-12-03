import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from utils import get_double, get_deviations

# Función de simulación con actualización dinámica
# Parámetros de la ventana de visualización
# Parámetros de la ventana de visualización
window_size = 1000  # Mostrar los últimos 1000 minutos

# Función de simulación con actualización dinámica
def run_simulation():
    global temperature, integral, previous_error, set_point, deviations, heater_power, perturbacion

    if times[-1] < total_time:
        for _ in range(60):  # Procesar 60 pasos (1 hora) por iteración
            if times[-1] >= total_time:
                break

            # Aplico los desvíos (si los hay)
            if deviations and times[-1] >= deviations[0][0]:
                deviation = deviations.pop(0)
                temperature += deviation[1]

            # Control PID
            error = set_point - temperature
            proportional = error
            integral += error * time_step
            derivative = (error - previous_error) / time_step

            control_signal = Kp * proportional + Ki * integral + Kd * derivative
            control_signal = max(min(control_signal, max_heating_rate), max_cooling_rate)

            if control_signal == max_heating_rate or control_signal == max_cooling_rate:
                integral -= error * time_step

            # Actualizar temperatura según el control y perturbaciones
            temperature += heat_transfer_coefficient * control_signal * time_step
            temperature += perturbacion
            perturbacion = 0  # Resetear perturbación después de aplicarla

            # Registrar datos para gráficos
            temperatures.append(temperature)
            times.append(times[-1] + time_step)
            heater_power.append(control_signal / max_heating_rate if control_signal > 0 else control_signal / max_cooling_rate)

            previous_error = error

        # Actualizar gráficos
        temp_line.set_data(times, temperatures)
        power_line.set_data(times, heater_power)

        # Ajustar ventana deslizante en el eje X
        if times[-1] > window_size:
            ax[0].set_xlim(times[-1] - window_size, times[-1])
            ax[1].set_xlim(times[-1] - window_size, times[-1])
        else:
            ax[0].set_xlim(0, window_size)
            ax[1].set_xlim(0, window_size)

        ax[0].relim()
        ax[0].autoscale_view(scaley=True)  # Solo ajustar el eje Y
        ax[1].relim()
        ax[1].autoscale_view(scaley=True)  # Solo ajustar el eje Y
        canvas.draw()

        # Llamar de nuevo
        root.after(100, run_simulation)



# Función para actualizar la perturbación
def agregar_perturbacion():
    global perturbacion
    try:
        perturbacion = float(temp_entry.get())
        temp_entry.delete(0, tk.END)  # Limpiar la entrada después de usarla
    except ValueError:
        pass

def on_closing():
    root.destroy()
    exit()

# Parámetros de simulación
time_step = 1  # Cada paso representa 1 minuto
dias = 30
total_time = dias*24*60  # 7 días (en minutos)
set_point = get_double("Ingrese la temperatura deseada del agua (°C): ", 20, 40)
initial_temperature = get_double("Ingrese la temperatura inicial del agua (°C): ", 10, 30)
deviations = get_deviations(1)  # Lista vacía si no se usan desvíos externos
perturbacion = 0

max_heating_rate = 0.5
max_cooling_rate = -0.5
heat_transfer_coefficient = 0.01
Kp = 0.3
Ki = 0.02
Kd = 0.01

temperature = initial_temperature
integral = 0
previous_error = set_point - temperature
temperatures = [temperature]
times = [0]
heater_power = [0]

# Crear ventana Tkinter
root = tk.Tk()
root.title("Simulación de Temperatura de Piscina")

frame = tk.Frame(root)
frame.pack()

temp_label = tk.Label(frame, text="Agregar perturbación:")
temp_label.grid(row=0, column=0)
temp_entry = tk.Entry(frame)
temp_entry.grid(row=0, column=1)
temp_button = tk.Button(frame, text="Aplicar", command=agregar_perturbacion)
temp_button.grid(row=0, column=2)

# Crear figura de Matplotlib
fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
temp_line, = ax[0].plot([], [], label='Temperatura del agua')
set_point_line, = ax[0].plot([0, total_time], [set_point, set_point], 'r--', label='Temperatura deseada')  # Línea fija
power_line, = ax[1].plot([], [], label='Potencia del climatizador')

ax[0].set_ylabel('Temperatura (°C)')
ax[0].set_title('Control de Temperatura de Piscina')
ax[0].legend()
ax[0].grid(True)

ax[1].set_xlabel('Tiempo (min)')
ax[1].set_ylabel('Potencia (normalizada)')
ax[1].set_title('Potencia del Climatizador')
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
canvas.draw()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar simulación
root.after(100, run_simulation)
root.mainloop()