import os
import shutil
import subprocess
import sys

# Nome do arquivo do seu programa
script_name = 'Pepe Browser.py'
# Ícone do seu aplicativo
icon_name = 'icon.ico'  # ou icon.png se você preferir

# Função para verificar se o PyInstaller está instalado
def check_pyinstaller():
    try:
        subprocess.run(['pyinstaller', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Instala o PyInstaller
def install_pyinstaller():
    print("PyInstaller não encontrado. Instalando...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

# Cria a pasta 'build' se não existir
build_dir = 'build'
os.makedirs(build_dir, exist_ok=True)

# Copia o ícone para a pasta 'build'
shutil.copy(icon_name, build_dir)

# Verifica se o PyInstaller está instalado
if not check_pyinstaller():
    install_pyinstaller()

# Comando do PyInstaller
command = [
    'pyinstaller',
    '--onefile',
    '--noconsole',
    f'--icon={os.path.join(build_dir, icon_name)}',  # Usa o ícone na nova pasta
    script_name
]

# Executa o comando
try:
    subprocess.run(command, check=True)
    print("Compilação concluída! O executável pode ser encontrado na pasta 'dist'.")
except subprocess.CalledProcessError as e:
    print(f"Erro na compilação: {e}")
