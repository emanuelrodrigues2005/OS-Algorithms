import time
import hashlib
import itertools

WORDLIST = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789"

class Security:
    @staticmethod
    def hash_password_sha256(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @classmethod
    def hash_breaker_sha256(cls, hashed_password, max_length=8, log_interval=100000):
        start_time = time.time()
        attempt_count = 0

        for length in range(1, max_length + 1):
            for combo in itertools.product(WORDLIST, repeat=length):
                attempt_count += 1
                attempt = ''.join(combo)

                if attempt_count % log_interval == 0:
                    print(f"{attempt_count // 1000}k tentativas já realizadas... Última tentativa: {attempt}")

                if cls.hash_password_sha256(attempt) == hashed_password:
                    end_time = time.time()
                    print(f"\nSenha descriptografada: {attempt}")
                    print(f"Tempo gasto: {end_time - start_time:.2f} segundos")
                    return attempt

        end_time = time.time()
        print("\nSenha não encontrada")
        print(f"Tempo gasto: {end_time - start_time:.2f} segundos")
        return None

if __name__ == "__main__":
    password = input("Insira a senha a ser criptografada (máx 8 caracteres): ")
    if len(password) > 8:
        print("Senha muito longa! Apenas os 8 primeiros caracteres serão usados.")
        password = password[:8]
    
    print("Criptografando a senha usando SHA-256...")
    time.sleep(0.5)
    hashed_password = Security.hash_password_sha256(password)
    print(f"Senha criptografada: {hashed_password}")
    
    print("Tentativa de descriptografia da senha...")
    Security.hash_breaker_sha256(hashed_password)