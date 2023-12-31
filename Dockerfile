# Imagen
FROM python:3.12-slim

# directorio de trabajo de la app
WORKDIR /main

# Copia los requerimientos del anfitrion
COPY requirements.txt ./requirements.txt

# Instala los requerimientos
RUN pip install -r requirements.txt

# Copia todo lo del anfitrion (clonado de github)
COPY main.py funcion_api.py 

# Argumentos para el comando entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]