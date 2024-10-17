import os
import shutil
import subprocess
import sys

# Nome do arquivo do seu programa
script_name = 'Pepe Browser.py'
# Ícone do seu aplicativo
icon_name = 'icon.ico'

# Função para verificar se o PyInstaller está instalado
def check_pyinstaller():
    try:
        subprocess.run(['pyinstaller', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Instala o PyInstaller se necessário
def install_pyinstaller():
    print("PyInstaller não encontrado. Instalando...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

# Verifica se o PyInstaller está instalado
if not check_pyinstaller():
    install_pyinstaller()

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
