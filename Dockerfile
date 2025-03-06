FROM python:3.13-slim-bookworm

RUN apt-get update && \
    apt-get -y install sudo && \
    sudo apt-get -y install jq

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . /app

RUN python3 -m pip install .

# Same as just raw-run and ust run
CMD sh ./raw_run.sh && \
    kedro run
