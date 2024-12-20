import os
import pyaes

def load_key():
    # Carrega a chave salva
    try:
        with open("key_storage.txt", "r") as key_file:
            key = bytes.fromhex(key_file.read().strip())
            if len(key) not in [16, 24, 32]:
                raise ValueError("Tamanho da chave inválido. Deve ser 16, 24 ou 32 bytes.")
            print(f"Chave carregada: {key.hex()}")
            return key
    except FileNotFoundError:
        print("Erro: Arquivo de chave não encontrado!")
        exit()
    except ValueError as e:
        print(f"Erro: {e}")
        exit()

def decrypt_file(file_path, key):
    # Abre o arquivo criptografado e descriptografa
    print(f"Descriptografando o arquivo: {file_path}")
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
            if not file_data:
                raise ValueError("O arquivo está vazio ou corrompido.")
            print(f"Dados criptografados lidos ({len(file_data)} bytes): {file_data[:32]}...")  # Mostra parte dos dados

        aes = pyaes.AESModeOfOperationCTR(key)
        decrypt_data = aes.decrypt(file_data)

        # Cria um arquivo descriptografado
        new_file = file_path.replace(".ransomwaretroll", "")
        with open(new_file, "wb") as decrypted_file:
            decrypted_file.write(decrypt_data)
        print(f"Arquivo {file_path} descriptografado com sucesso em {new_file}.")
    except Exception as e:
        print(f"Erro ao descriptografar {file_path}: {e}")

if __name__ == "__main__":
    file_to_decrypt = input("Digite o caminho do arquivo que deseja descriptografar: ").strip()
    file_to_decrypt = file_to_decrypt.strip('"')  # Remove aspas extras, se existirem
    key = load_key()
    decrypt_file(file_to_decrypt, key)
