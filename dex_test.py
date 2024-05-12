# pycryptodome 모듈 설치하셔야합니다
# apktool도 다운받아주세요
# 디렉토리는 각자 환경에 맞춰 설정하셔야합니다


import subprocess
from Crypto.Cipher import AES 
from Crypto.Util.Padding import unpad
import os

#java설치확인
def find_java_binary():
    java_home = os.environ.get('JAVA_HOME')
    if java_home:
        return os.path.join(java_home, 'bin', 'java')
    return 'java'

#apk 언패킹 output_dir은 꼭 아무것도 없는 폴더에 해주세요!!! 안그럼 파일 다 날라갑니다!!!
def unpack_apk(apk_path, output_dir, apktool_path='apktool.jar'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    java_path = find_java_binary()
    command = [java_path, '-jar', apktool_path, 'd', '--no-src', apk_path, '-o', output_dir, '-f']

    try:
        subprocess.run(command, check=True, text=True)
        print(f"APK has been successfully unpacked to {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to unpack APK: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

#apk 리패킹
def repack_apk(source_dir, apktool_path='apktool.jar'):
    java_path = find_java_binary()
    command = [java_path, '-jar', apktool_path, 'b', source_dir, '-o', f"{source_dir}_repacked.apk"]

    try:
        subprocess.run(command, check=True, text=True)
        print(f"APK has been successfully repacked from {source_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to repack APK: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

#암호화 dex파일찾기 위해, dex파일부터 찾기
def find_encrypted_dex(directory):
    dex_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".dex"):
                file_path = os.path.join(root, file)
                if is_encrypted(file_path):
                    dex_files.append(file_path)
    return dex_files

#암호화 dex파일찾기(masic num 이용)
def is_encrypted(file_path):
    with open(file_path, 'rb') as file:
        magic_number = file.read(4)
        if magic_number != b'dex\n':
            return True
        else:
            return False

#복호화
def decrypt_aes_ecb(encrypted_data, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data

def read_encrypted_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def save_decrypted_file(file_path, decrypted_data):
    # 원본 파일에 복호화된 데이터를 덮어쓰기
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

def main():
    apk_path = 'C:\\Users\\siriu\\Downloads\\sample.apk'
    output_dir = 'C:\\Users\\siriu\\Downloads\\sample_de'
    apktool_path = 'C:\\Windows\\apktool.jar'
    key = 'dbcdcfghijklmaop'  # 16바이트 AES 키

    unpack_apk(apk_path, output_dir, apktool_path)
    encrypted_dex_files = find_encrypted_dex(output_dir)
    print("Encrypted DEX files:", encrypted_dex_files)

    for file_path in encrypted_dex_files:
        encrypted_data = read_encrypted_file(file_path)
        decrypted_data = decrypt_aes_ecb(encrypted_data, key)
        save_decrypted_file(file_path, decrypted_data)
        print(f"Decrypted data has been written back to {file_path}")
        
    repack_apk(output_dir, apktool_path)

if __name__ == '__main__':
    main()

