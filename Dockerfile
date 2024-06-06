# Usar una imagen base oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requerimientos al contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el contenido del directorio actual en el contenedor
COPY . .

# Establecer la variable de entorno para desactivar el buffering de Python (opcional)
ENV PYTHONUNBUFFERED 1

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.__main__:app"]
