import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Configuración del archivo
# Cambia este nombre por el de tu lectura más reciente
file_path = 'data/Viernes_PM_VAN_IDA_1771028361625.csv'
nombre_archivo = os.path.basename(file_path)

# 2. Cargar y preparar datos
df = pd.read_csv(file_path)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['rel_time'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

# Separar datos del sensor de las marcas manuales
df_sensor = df[df['tipo'] == 'STREAM'].copy()
df_manual = df[df['tipo'] == 'MANUAL'].copy()

# 3. Crear Visualización de 3 niveles
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

# --- GRÁFICA 1: ACELERÓMETRO (ax, ay, az) ---
ax1.plot(df_sensor['rel_time'], df_sensor['ax'], label='X (Lateral)', alpha=0.6)
ax1.plot(df_sensor['rel_time'], df_sensor['ay'], label='Y (Longitudinal)', alpha=0.6)
ax1.plot(df_sensor['rel_time'], df_sensor['az'], label='Z (Vertical)', alpha=0.9, color='blue')
ax1.set_title(f'Análisis de Viaje: {nombre_archivo}\n\nAcelerómetro (Impactos)', fontsize=14)
ax1.set_ylabel('m/s²')

# --- GRÁFICA 2: GIROSCOPIO (gx, gy, gz) ---
# El eje 'gx' suele ser el Pitch (cabeceo) si el celular va plano con pantalla arriba
ax2.plot(df_sensor['rel_time'], df_sensor['gx'], label='X (Pitch/Cabeceo)', color='darkgreen')
ax2.plot(df_sensor['rel_time'], df_sensor['gy'], label='Y (Roll/Inclinación)', alpha=0.5)
ax2.plot(df_sensor['rel_time'], df_sensor['gz'], label='Z (Yaw/Giro)', alpha=0.5)
ax2.set_title('Giroscopio (Rotación y Balanceo del Vehículo)', fontsize=12)
ax2.set_ylabel('rad/s')

# --- GRÁFICA 3: MAGNITUD TOTAL ---
ax3.plot(df_sensor['rel_time'], df_sensor['mag'], color='black', linewidth=1.5, label='Magnitud Combinada')
ax3.axhline(y=0.4, color='orange', linestyle=':', label='Umbral Sugerido (0.4)')
ax3.set_title('Magnitud Resultante', fontsize=12)
ax3.set_ylabel('Magnitud')
ax3.set_xlabel('Tiempo (segundos)')

# 4. Dibujar Marcas Manuales en todas las gráficas
for t in df_manual['rel_time']:
    for ax in [ax1, ax2, ax3]:
        ax.axvline(x=t, color='red', linestyle='--', linewidth=2, 
                   label='MARCA MANUAL' if t == df_manual['rel_time'].iloc[0] and ax == ax1 else "")

# Ajustes finales de estilo
for ax in [ax1, ax2, ax3]:
    ax.legend(loc='upper right', fontsize='small')
    ax.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.show()

# Resumen de la sesión
print(f"--- Resumen de la lectura ---")
print(f"Duración: {round(df['rel_time'].max(), 2)} segundos")
print(f"Registros de sensores: {len(df_sensor)}")
print(f"Topes marcados manualmente: {len(df_manual)}")