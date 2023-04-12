import sys
from cx_Freeze import setup, Executable

base = "Win32GUI" if sys.platform == "win32" else None
includefiles = ['templates', 'static']

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

build_exe_options = {
    'build_exe': {
        'build_exe': 'build',
        'include_files': includefiles,
        "zip_include_packages": requirements
    }
}

setup(
    name='data_app',
    version = '1.0',
    description = 'Data Mining App',
    options = build_exe_options,
    executables = [
        Executable(
            script='app.py',
            target_name='data_mining_app.exe'
        )
    ]
)