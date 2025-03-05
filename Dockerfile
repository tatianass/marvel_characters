FROM python:3.13

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . /app

RUN python3 -m pip install .

COPY src /app

CMD python3 -m marvel_characters.main
