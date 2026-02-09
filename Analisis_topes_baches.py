import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar el archivo (Asegúrate de poner el nombre correcto de tu archivo)
#file_path = 'data/sesion_1770608727083.csv'
#file_path = 'data/sesion_1770638989431.csv'
#file_path = 'data/sesion_1770639148633.csv'
#file_path = 'data/sesion_1770642504456.csv'
#file_path = 'data/sesion_1770642647648.csv'
file_path = 'data/sesion_1770644854393.csv'
#file_path = 'data/sesion_1770645428606.csv' # Caminar
#file_path = 'data/sesion_1770645524700.csv' # Subir escaleras
df = pd.read_csv(file_path)

# 2. Convertir el timestamp ISO 8601 a objetos datetime y calcular tiempo relativo
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['rel_time'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()

# 3. Visualización
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Gráfica de Ejes Crudos (X, Y, Z)
ax1.plot(df['rel_time'], df['x_raw'], label='X (Lateral)', alpha=0.7)
ax1.plot(df['rel_time'], df['y_raw'], label='Y (Longitudinal)', alpha=0.7)
ax1.plot(df['rel_time'], df['z_raw'], label='Z (Vertical)', alpha=0.7)
ax1.set_title('Señales Crudas del Acelerómetro (Bolsa del Pantalón)')
ax1.set_ylabel('Aceleración (m/s²)')
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.6)

# Gráfica de Magnitud Filtrada (La que usa tu App)
ax2.plot(df['rel_time'], df['magnitude_filtered'], color='black', linewidth=1.5, label='Magnitud (Filtrada)')
# Línea de umbral sugerida (0.4)
ax2.axhline(y=0.4, color='red', linestyle=':', label='Umbral Sugerido')

ax2.set_title('Magnitud del Vector Suavizada')
ax2.set_xlabel('Tiempo desde el inicio (segundos)')
ax2.set_ylabel('Magnitud')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()