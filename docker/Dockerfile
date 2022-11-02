# docker/backend/Dockerfile
FROM python:3.9.0-alpine
# set working directory
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app
# adding logs dir
RUN mkdir logs
RUN cd logs && touch app.log www.log

RUN apk update
RUN apk add bash && apk --no-cache add dos2unix
RUN apk --no-cache add mariadb-client
RUN apk add --no-cache mariadb-dev build-base
RUN apk add --no-cache libressl-dev musl-dev libffi-dev
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install mysqlclient

ADD . /usr/src/app
# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt
# install requirements
RUN python -m pip install --upgrade pip
RUN pip install --no-cache -r requirements.txt
RUN pip freeze > requirements.txt
# add entrypoint.sh
ADD ./entrypoint.sh /usr/src/app/entrypoint.sh
# execute permission to entrypoint
RUN chmod +x ./entrypoint.sh
RUN dos2unix ./entrypoint.sh && apk del dos2unix
# add app
EXPOSE 5000
# run server
CMD ["sh", "./entrypoint.sh"]