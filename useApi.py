import requests

# Endpoint API
API_URL = "http://127.0.0.1:5000/check_password"

# Password yang ingin dicek

password_to_check = input("Masukkan Password : ")

# Data untuk dikirimkan ke API
data = {
    "password": password_to_check
}

try:
    # Mengirim permintaan POST ke API
    response = requests.post(API_URL, json=data)

    # Memeriksa apakah permintaan berhasil
    if response.status_code == 200:
        result = response.json()
        # Extract the check_results from the response
        check_results = result.get('check_results', {})

        print("Hasil pengecekan password:")
        print(f"Password: {check_results.get('password')}")
        print(f"Strength: {check_results.get('strength_check')}")
        print(f"Wordlist Check: {check_results.get('wordlist_check')}")
        print(f"Breach Check: {check_results.get('breach_check')}")
    else:
        print(f"Error: {response.status_code}, {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
