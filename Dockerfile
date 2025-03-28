FROM python:3.8-slim-buster

WORKDIR /jellyfin_sports

RUN pip install jellyfin_sports==1.0.7 --no-binary=jellyfin_sports

CMD [ "python3", "-m" , "jellyfin_sports", "run", "-a", "-o", "/jellyfin_sports/output"]
