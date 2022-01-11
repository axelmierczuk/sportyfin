FROM python:3.8-slim-buster

WORKDIR /sportyfin

COPY . .

RUN pip install . --no-binary=sportyfin

CMD [ "python3", "-m" , "sportyfin", "run", "-a", "-o", "/sportyfin/output"]