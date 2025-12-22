# File: generate_hash.py
from werkzeug.security import generate_password_hash

# Password yang akan di-hash (sesuaikan jika Anda ingin password lain)
password_to_hash = 'admin123' 

# Generate hash
hashed_password = generate_password_hash(password_to_hash)

print("-" * 50)
print(f"Password Asli: {password_to_hash}")
print(f"Hash Baru (untuk diupdate ke SQL):")
print(hashed_password)
print("-" * 50)
print("\nInstruksi:")
print("1. Salin hash di atas.")
print("2. Update kolom 'password' untuk user 'admin' di database 'balladigital' menggunakan hash ini.")
print("3. Restart Flask dan coba login lagi.")