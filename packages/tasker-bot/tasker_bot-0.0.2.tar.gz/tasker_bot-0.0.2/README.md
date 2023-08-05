# tasker_bot

# Comandos de Actualización del Código
####Borramos la carpeta base de distribución
rm -rf dist/

####Generamos nuevamente losarchivos de la versión
python3 setup.py sdist bdist_wheel

####Enviamos la actualización
twine upload --repository-url https://upload.pypi.org/legacy/  dist/*


Comando de control y gestión de tareas.