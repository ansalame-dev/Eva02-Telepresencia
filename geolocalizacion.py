import urllib.parse
import requests

# ==========================================================
# Evaluación Parcial - Ítem 3: Geolocalización con GraphHopper
# Integrantes: Angel Salame, Alex Formas, Gonzalo Diaz
# ==========================================================

# URLs base de GraphHopper
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
idioma = "es"

# REEMPLAZA ESTA LÍNEA con tu API Key real obtenida en GraphHopper
key = "d27bfde8-179d-42dd-9ae7-cc5475500a10"


def obtener_coordenadas(lugar):
  """Función para buscar lat y lon de un lugar usando GraphHopper Geocoding"""
  params = {"q": lugar, "locale": idioma, "key": key}
  url = geocode_url + urllib.parse.urlencode(params)
  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    if data.get("hits"):
      point = data["hits"][0]["point"]
      return point["lat"], point["lng"]
  return None


def main():
  print("==================================================")
  print("   SISTEMA DE GEOLOCALIZACIÓN Y RUTAS (GRAPHHOPPER)")
  print("   Integrantes: Angel Salame, Alex Formas, Gonzalo Diaz")
  print("==================================================")
  print("💡 Escribe 's' o 'salir' en cualquier momento para terminar.\n")

  if key == "TU_API_KEY_AQUI":
    print(
        "⚠️ ADVERTENCIA: Debes colocar tu API Key real de GraphHopper en la"
        " variable 'key' antes de realizar peticiones.\n"
    )

  while True:
    # Ingreso de Origen
    origen_input = (
        input("Ingrese lugar de Origen (ej: Santiago, Chile): ")
        .strip()
        .lower()
    )
    if origen_input in ["s", "salir"]:
      print("\n👋 Finalizando sistema de geolocalización. ¡Hasta luego!")
      break

    coords1 = obtener_coordenadas(origen_input)
    if not coords1:
      print(
          "⚠️ No se encontró la ubicación de origen o la API Key es inválida."
          " Intente nuevamente.\n"
      )
      continue
    lat1, lon1 = coords1

    # Ingreso de Destino
    destino_input = (
        input("Ingrese lugar de Destino (ej: Valparaíso, Chile): ")
        .strip()
        .lower()
    )
    if destino_input in ["s", "salir"]:
      print("\n👋 Finalizando sistema de geolocalización. ¡Hasta luego!")
      break

    coords2 = obtener_coordenadas(destino_input)
    if not coords2:
      print(
          "⚠️ No se encontró la ubicación de destino. Intente nuevamente.\n"
      )
      continue
    lat2, lon2 = coords2

    # Petición de ruta a GraphHopper
    url_ruta = (
        f"{route_url}point={lat1},{lon1}&point={lat2},{lon2}&vehicle=car"
        f"&locale={idioma}&key={key}"
    )
    res_route = requests.get(url_ruta)

    if res_route.status_code == 200:
      data_route = res_route.json()
      if "paths" in data_route and len(data_route["paths"]) > 0:
        path = data_route["paths"][0]

        # Distancia en metros convertida a km y redondeada a 2 decimales
        distancia_km = round(path["distance"] / 1000.0, 2)
        # Tiempo en milisegundos convertido a minutos y redondeado a 2 decimales
        tiempo_minutos = round(path["time"] / 60000.0, 2)

        # Generar narrativa del viaje
        print("\n" + "=" * 50)
        print("🧭 REPORTE DE TRAYECTORIA Y NARRATIVA (GRAPHHOPPER)")
        print("=" * 50)
        print(f"• Origen buscado: {origen_input.title()} ({lat1}, {lon1})")
        print(f"• Destino buscado: {destino_input.title()} ({lat2}, {lon2})")
        print(f"• Distancia total calculada: **{distancia_km} km**")
        print(f"• Tiempo estimado de trayecto: **{tiempo_minutos} minutos**")
        print(
            "• Estado de la ruta: Trayecto optimizado mediante motor"
            " GraphHopper."
        )
        print("=" * 50 + "\n")
      else:
        print("⚠️ No se pudo calcular la ruta entre los puntos especificados.\n")
    else:
      print(
          f"⚠️ Error al consultar la API de rutas: {res_route.status_code} -"
          f" {res_route.text}\n"
      )


if __name__ == "__main__":
  main()