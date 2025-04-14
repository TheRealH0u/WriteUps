FROM python:3.12-slim

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install gcc
RUN apt-get update && apt-get install -y gcc wget unzip && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt /app/
RUN python -m pip install -r /app/requirements.txt

ARG TEMPLATES_VERSION
RUN wget https://github.com/projectdiscovery/nuclei-templates/archive/refs/tags/v${TEMPLATES_VERSION}.zip -O /tmp/nuclei-templates.zip && unzip /tmp/nuclei-templates.zip -d /app/ && rm /tmp/nuclei-templates.zip && mv /app/nuclei-templates-${TEMPLATES_VERSION} /app/nuclei-templates

WORKDIR /app
COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:443", "--threads", "3", "--keyfile", "/cert/privkey.pem", "--certfile", "/cert/fullchain.pem", "webserver:app"]
