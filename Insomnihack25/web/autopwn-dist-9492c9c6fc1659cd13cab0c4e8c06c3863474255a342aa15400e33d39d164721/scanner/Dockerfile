ARG PLAYWRIGHT_VERSION
FROM mcr.microsoft.com/playwright:v${PLAYWRIGHT_VERSION}

ARG NUCLEI_VERSION
ARG TEMPLATES_VERSION

RUN apt-get update && apt-get install -y at wget unzip git && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/projectdiscovery/nuclei/releases/download/v${NUCLEI_VERSION}/nuclei_${NUCLEI_VERSION}_linux_amd64.zip -O /tmp/nuclei.zip && unzip /tmp/nuclei.zip nuclei -d /usr/local/bin/ && rm /tmp/nuclei.zip

RUN mkdir /scanner
WORKDIR /scanner

COPY run.sh /scanner/
RUN chmod +x /scanner/run.sh

RUN wget https://github.com/projectdiscovery/nuclei-templates/archive/refs/tags/v${TEMPLATES_VERSION}.zip -O /tmp/nuclei-templates.zip && unzip /tmp/nuclei-templates.zip -d /scanner/ && rm /tmp/nuclei-templates.zip && mv /scanner/nuclei-templates-${TEMPLATES_VERSION} /scanner/nuclei-templates

RUN nuclei -update-templates -headless 2>/dev/null

COPY ./flag.txt /flag.txt

ENTRYPOINT ["/scanner/run.sh"]
