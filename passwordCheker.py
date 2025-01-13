def passwordChecker(password):
    # Kriteria
    caps = any(c.isupper() for c in password)  # Apakah ada karakter kapital
    lowr = any(c.islower() for c in password)  # Apakah ada karakter kecil
    nums = any(c.isdigit() for c in password)  # Apakah ada karakter angka
    symb = any(c in '!@#$%^&' for c in password)  # Apakah ada karakter simbol
    length_Mediumvalid = len(password) >= 8  # Panjang minimal 8 untuk valid
    length_Strongvalid = len(password) >= 12  # Panjang minimal 12 untuk strong

    # Return "Strong" jika semua kriteria terpenuhi dan panjang >= 12
    if caps and lowr and nums and symb and length_Strongvalid:
        return "Strong"
    # Return "Medium" jika semua kriteria terpenuhi tetapi panjang < 12
    elif caps and lowr and nums and symb and length_Mediumvalid:
        return "Medium"
    else:
        return "Weak"

# Input dari pengguna
password = input("Masukkan password anda: ")

# Validasi password
status = passwordChecker(password)
if status == "Strong":
    print("Password sangat kuat! (Strong)")
elif status == "Medium":
    print("Password cukup kuat. (Medium)")
else:
    print("Password terlalu lemah. Pastikan memenuhi semua kriteria.")
