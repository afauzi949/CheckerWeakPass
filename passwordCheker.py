def load_seclist(file_path):
    # Memuat password dari seclist (file txt)
    with open(file_path, 'r') as file:
        return {line.strip() for line in file}  # Menggunakan set untuk efisiensi pencarian

def passwordChecker(password, seclist):
    # Kriteria
    caps = any(c.isupper() for c in password)  # Apakah ada karakter kapital
    lowr = any(c.islower() for c in password)  # Apakah ada karakter kecil
    nums = any(c.isdigit() for c in password)  # Apakah ada karakter angka
    symb = any(c in '!@#$%^&' for c in password)  # Apakah ada karakter simbol
    length_Mediumvalid = len(password) >= 8  # Panjang minimal 8 untuk valid
    length_Strongvalid = len(password) >= 12  # Panjang minimal 12 untuk strong

    # Mengecek apakah password ada dalam seclist
    if password in seclist:
        return "Password berada dalam daftar password umum. Silakan pilih yang lain."

    # Return "Strong" jika semua kriteria terpenuhi dan panjang >= 12
    if caps and lowr and nums and symb and length_Strongvalid:
        return "Strong"
    # Return "Medium" jika semua kriteria terpenuhi tetapi panjang < 12
    elif caps and lowr and nums and symb and length_Mediumvalid:
        return "Medium"
    else:
        return "Weak"

# Memuat daftar seclist dari file
seclist = load_seclist('seclist.txt')  # Pastikan file 'seclist.txt' ada dan berisi password umum

# Input dari pengguna
password = input("Masukkan password anda: ")

# Validasi password
status = passwordChecker(password, seclist)
if status == "Strong":
    print("Password sangat kuat! (Strong)")
elif status == "Medium":
    print("Password cukup kuat. (Medium)")
else:
    print(status)  # Menampilkan pesan "Weak" atau alasan lainnya
