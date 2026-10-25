import random
import requests

BASE_URL = "http://library.demo.local/api/v1"
LOGIN_URL = f"{BASE_URL}/loginViaBasic"
url = f"{BASE_URL}/books"

print("🔄 Autenticándose en la API...")
auth_resp = requests.post(LOGIN_URL, auth=("cisco", "Cisco123!"))

if auth_resp.status_code == 200:
  token = auth_resp.json().get("token")
  print("✅ ¡Token obtenido con éxito!\n")
else:
  print(f"❌ Error al autenticar: {auth_resp.status_code}")
  exit()

# LA CLAVE ESTÁ AQUÍ: La API exige exactamente esta cabecera
headers = {"X-API-KEY": token, "Content-Type": "application/json"}

autores = [
    "Angel Salame",
    "Alex Formas",
    "Gonzalo Diaz",
]

tematicas = [
    "Redes inalambricas",
    "Seguridad Perimetral",
    "Automatizacion NetDevOps",
    "Fundamentos Cloud",
    "Python para Redes",
]

print("📚 Iniciando inserción masiva de 50 libros...")

# Usamos el rango de IDs del 10 al 59 tal como lo tenía tu amigo
for i in range(10, 60):
  autor_aleatorio = random.choice(autores)
  titulo_aleatorio = f"{random.choice(tematicas)} Vol. {i}"
  isbn_aleatorio = "".join([str(random.randint(0, 9)) for _ in range(10)])

  nuevo_libro = {
      "id": i,
      "title": titulo_aleatorio,
      "author": autor_aleatorio,
      "isbn": isbn_aleatorio,
  }

  response = requests.post(url, json=nuevo_libro, headers=headers)

  if response.status_code in [200, 201]:
    print(f"Libro ID {i} creado - Estado HTTP: {response.status_code} | {titulo_aleatorio}")
  else:
    print(f"⚠️ Error al crear libro ID {i}: {response.status_code} - {response.text}")

print("\n¡Proceso de inserción masiva finalizado con éxito!")