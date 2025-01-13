def passwordChecker(password):
    #kriteria
    caps = any(c.isupper() for c in password)  # Apakah ada huruf kapital
    nums = any(c.isdigit() for c in password)  # Apakah ada angka
    symb = any(c in '!@#$%^&' for c in password)  # Apakah ada simbol
    length_valid = len(password) >= 8  # Panjang password cukup

    # Return True jika semua kriteria terpenuhi
    return caps and nums and symb and length_valid

# Input dari pengguna
password = input("Masukkan password anda: ")

# Validasi password
if passwordChecker(password):
    print("Password valid!")
else:
    print("Password tidak valid. Pastikan memenuhi semua kriteria.")
