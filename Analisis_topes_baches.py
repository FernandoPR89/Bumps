import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar el nuevo archivo
file_path = 'data/viaje_1770688696371.csv'
df = pd.read_csv(file_path)

# 2. Preparación de datos
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['rel_time'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

# Separamos los datos del sensor (STREAM) de las marcas manuales (MANUAL)
df_sensor = df[df['tipo'] == 'STREAM'].copy()
df_manual = df[df['tipo'] == 'MANUAL'].copy()

# 3. Visualización Pro
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# --- GRÁFICA 1: EJES X, Y, Z ---
ax1.plot(df_sensor['rel_time'], df_sensor['x'], label='X (Lateral)', alpha=0.7)
ax1.plot(df_sensor['rel_time'], df_sensor['y'], label='Y (Longitudinal)', alpha=0.7)
ax1.plot(df_sensor['rel_time'], df_sensor['z'], label='Z (Vertical)', alpha=0.7)

# Dibujar líneas rojas donde presionaste el botón MANUAL
for t in df_manual['rel_time']:
    ax1.axvline(x=t, color='red', linestyle='--', linewidth=2, label='MARCA MANUAL' if t == df_manual['rel_time'].iloc[0] else "")

ax1.set_title('Señales del Acelerómetro con Marcas Manuales')
ax1.set_ylabel('Aceleración (m/s²)')
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.5)

# --- GRÁFICA 2: MAGNITUD ---
ax2.plot(df_sensor['rel_time'], df_sensor['mag'], color='black', linewidth=1.5, label='Magnitud (Sensor)')
ax2.axhline(y=0.4, color='orange', linestyle=':', label='Umbral 0.4')

# También ponemos las marcas manuales aquí
for t in df_manual['rel_time']:
    ax2.axvline(x=t, color='red', linestyle='--', linewidth=2)

ax2.set_title('Análisis de Magnitud y Detección')
ax2.set_xlabel('Tiempo desde el inicio (segundos)')
ax2.set_ylabel('Magnitud')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

# Resumen científico para tu bitácora
print(f"Puntos de sensor registrados: {len(df_sensor)}")
print(f"Topes marcados manualmente: {len(df_manual)}")