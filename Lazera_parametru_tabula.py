import pandas as pd
import itertools

# --- Fiber 20W lāzera parametru fiksētie dati ---
laser_params = {
    "Jauda (%)": 70,        # nemainīga jauda
    "Lāzera tips": "Fiber 20W"
}

# --- Mainīgie parametri ---
start_angles = [0, 10, 20]       # piemērs: start angle
angle_steps = [5, 10, 15]        # piemērs: angle step
repeats = [1, 2, 3]              # atkārtojumu skaits
speeds = [100, 200, 300]         # ātrums, piemērs

# --- Izveido kombinācijas ar itertools.product ---
combinations = list(itertools.product(start_angles, angle_steps, repeats, speeds))

# --- Sagatavo datus tabulai ---
data = []
for comb in combinations:
    start_angle, angle_step, repeat, speed = comb
    row = {
        "Jauda (%)": laser_params["Jauda (%)"],
        "Lāzera tips": laser_params["Lāzera tips"],
        "Start angle (°)": start_angle,
        "Angle step (°)": angle_step,
        "Atkārtojumi": repeat,
        "Ātrums (mm/s)": speed
    }
    data.append(row)

# --- Izveido pandas DataFrame ---
df = pd.DataFrame(data)

# --- Saglabā Excel failā ---
df.to_excel("laser_fiber_20W_autotable.xlsx", index=False)

# --- Parāda tabulas priekšskatījumu ---
print(df.head(10))
