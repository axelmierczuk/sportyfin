FROM python:3.8-slim-buster

WORKDIR /sportyfin

RUN pip install sportyfin --no-binary=sportyfin

COPY . .

CMD [ "python3", "-m" , "sportyfin", "run", "-a", "-o", "/sportyfin/output"]