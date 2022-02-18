FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /usr/src/AlbumApp

COPY ./requierements.txt /usr/src/AlbumApp/requirements.txt
RUN pip install -r /usr/src/AlbumApp/requirements.txt

COPY . .

EXPOSE 8000