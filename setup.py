import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [],
    "excludes": [],
    "includes": [],
    "include_files": [],
    "optimize": 2
}

base = None

if sys.platform == "win32":
    base = "Win32GUI"  # Use isso se seu script não tiver uma janela de console

executables = [
    Executable("main.pyw", base=base)
]

setup(
    name="Nome do Executável",
    version="1.0",
    description="Descrição do Executável",
    options={"build_exe": build_exe_options},
    executables=executables
)