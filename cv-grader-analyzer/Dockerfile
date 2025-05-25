FROM python:3.11.12-slim

WORKDIR /grader-analyzer

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends gcc libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# RUN python -m pip install pip-tools

COPY ./requirements.txt /grader-analyzer/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /grader-analyzer/requirements.txt

COPY . /grader-analyzer/

CMD ["python", "main.py"]