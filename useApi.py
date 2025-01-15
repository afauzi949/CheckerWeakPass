import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

# Endpoint API
API_URL = "http://127.0.0.1:5000/check_password"

# Meminta input password dari pengguna
password_to_check = input("Masukkan Password: ")

# Data untuk dikirimkan ke API
data = {
    "password": password_to_check
}

try:
    # Mengirim request POST ke API
    response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        result = response.json()
        # Extract the check_results from the response
        check_results = result.get('check_results', {})
        
        # Membuat tabel hasil pengecekan
        table = Table(title="Hasil Pengecekan Password", box=box.ROUNDED)
        table.add_column("Kriteria", style="bold cyan", justify="left")
        table.add_column("Hasil", style="bold green", justify="left")

        # Menambahkan baris ke tabel
        table.add_row("Password", check_results.get('password', 'Tidak Tersedia'))
        table.add_row("Strength Check", check_results.get('strength_check', 'Tidak Tersedia'))
        table.add_row("Wordlist Check", check_results.get('wordlist_check', 'Tidak Tersedia'))
        table.add_row("Breach Check", check_results.get('breach_check', 'Tidak Tersedia'))
        
        console.print(Panel.fit(table, title="Password Checker", border_style="bold blue"))
    else:
        console.print(f"[bold red]Error:[/bold red] {response.status_code}, {response.text}")
except requests.exceptions.RequestException as e:
    console.print(f"[bold red]Request failed:[/bold red] {e}")
