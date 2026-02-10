import pandas as pd
import plotly.express as px

# 1. Cargar el archivo
file_path = 'data/viaje_1770688696371.csv' # Asegúrate que sea el nombre correcto
df = pd.read_csv(file_path)

# 2. Filtrar solo puntos con GPS válido
df_gps = df[(df['lat'] != 0.0) & (df['long'] != 0.0)].copy()

if df_gps.empty:
    print("Error: No se encontraron coordenadas GPS válidas en el archivo.")
else:
    # --- TRUCO PARA QUE SE VEAN LOS MARCADORES ---
    # Creamos una columna 'tamano_visual'. 
    # Si es MANUAL, le damos tamaño fijo (ej. 10). 
    # Si es AUTO, multiplicamos su magnitud para que se note (ej. mag * 20).
    def calcular_tamano(row):
        if row['tipo'] == 'MANUAL':
            return 2.0  # Tamaño fijo para marcas manuales (se verá grande)
        else:
            return max(0.5, row['mag']) # Para que los automáticos pequeños no desaparezcan

    df_gps['tamano_visual'] = df_gps.apply(calcular_tamano, axis=1)

    # 3. Crear el mapa interactivo
    fig = px.scatter_mapbox(
        df_gps, 
        lat="lat", 
        lon="long", 
        color="tipo",       # Diferente color para MANUAL vs AUTO
        size="tamano_visual", # Usamos nuestra nueva métrica de tamaño
        size_max=15,        # Tamaño máximo del punto en píxeles
        hover_data={        # Qué mostrar al pasar el mouse
            "timestamp": True, 
            "mag": True, 
            "tamano_visual": False, # Ocultamos la métrica auxiliar
            "lat": False, 
            "long": False
        }, 
        zoom=14, 
        title="Mapa de Topes Identificados"
    )

    # 4. Estilos
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

    # 5. Guardar y mostrar
    output_file = "mapa_topes_corregido.html"
    fig.write_html(output_file)
    print(f"¡Listo! Abre '{output_file}' para ver tus marcadores.")
    fig.show()