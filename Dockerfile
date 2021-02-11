FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR '/app'
COPY ./app/requirements.txt ./
RUN pip3 install -r /app/requirements.txt

COPY ./app ./
