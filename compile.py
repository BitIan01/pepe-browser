import os
import shutil
import subprocess
import sys

# Nome do arquivo do seu programa
script_name = 'Glide Browser.py'
# Ícone do seu aplicativo
icon_name = 'icon.ico'

# Função para verificar se um pacote está instalado
def check_package(package):
    try:
        subprocess.run([sys.executable, '-m', package, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Função para instalar um pacote
def install_package(package):
    print(f"{package} não encontrado. Instalando...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Verifica e instala PyInstaller, PyQt5 e PyQtWebEngine
packages = ['pyinstaller', 'PyQt5', 'PyQtWebEngine']

for package in packages:
    if not check_package(package):
        install_package(package)

# Comando do PyInstaller
command = [
    'pyinstaller',
    '--onefile',
    '--noconsole',
    f'--icon={icon_name}',  # Usa o ícone direto
    script_name
]

# Executa o comando do PyInstaller
try:
    subprocess.run(command, check=True)
    print("Compilação concluída! O executável pode ser encontrado na pasta 'dist'.")

    # Copia o ícone para a pasta 'dist'
    dist_dir = 'dist'
    os.makedirs(dist_dir, exist_ok=True)
    shutil.copy(icon_name, os.path.join(dist_dir, icon_name))
    print(f"O ícone foi copiado para a pasta '{dist_dir}'.")
except subprocess.CalledProcessError as e:
    print(f"Erro na compilação: {e}")
