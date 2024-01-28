FROM python:3.12

WORKDIR /discord_app

COPY ./requirements.txt /discord_app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./discord_app /discord_app

CMD [ "python", "main.py" ]