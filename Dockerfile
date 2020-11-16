# OS
FROM ubuntu:20.04

# python3 y pip
RUN apt update
RUN apt install -y python3-pip
RUN apt clean

# Requerimientos de la aplicación
RUN pip3 install virtualenv
RUN pip3 install gunicorn
RUN pip3 install django
RUN pip3 install django-widget-tweaks
RUN pip3 install django-crispy-forms

# Se expone el puerto 8000
EXPOSE 8000

# Copia al file Taller
ADD . /Taller
COPY . /Taller

# Otorgan permisos
RUN chown -R www-data:www-data /Taller
RUN chmod a+x /Taller/manage.py

# Workbench
WORKDIR /Taller

# Servidor
CMD python3 manage.py runserver 127.0.0.1:8000
