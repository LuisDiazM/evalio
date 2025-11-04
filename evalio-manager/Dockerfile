FROM python:3.11.12-slim

WORKDIR /evalio-manager

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# RUN python -m pip install pip-tools

COPY ./requirements.txt /evalio-manager/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /evalio-manager/requirements.txt

COPY . /evalio-manager/

CMD ["python", "main.py"]
