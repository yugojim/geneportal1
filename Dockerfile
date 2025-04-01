# Set default image base FROM python:3.9.15
FROM python:3.8

RUN apt-get update

RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx supervisor nano

ADD . /server
WORKDIR /server

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN useradd --no-create-home nginx

COPY nginx.conf /etc/nginx/sites-enabled/
#COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY uwsgi.ini /etc/
COPY supervisord.conf /etc/
#COPY ssl.csr /etc/nginx/ssl.csr
#COPY ssl.key /etc/nginx/ssl.key
CMD ["/usr/bin/supervisord"]
#CMD ["uwsgi", "uwsgi.ini"]
#CMD ["python manage.py runserver 0:8000"]
EXPOSE 8000
#EXPOSE 443