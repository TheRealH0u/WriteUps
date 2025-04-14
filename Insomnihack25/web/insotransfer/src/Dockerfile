FROM ubuntu@sha256:3afff29dffbc200d202546dc6c4f614edc3b109691e7ab4aa23d02b42ba86790

RUN groupadd --system g-insotransfer && useradd --system u-insotransfer --group g-insotransfer

COPY python .
RUN apt update 
RUN apt install -y "./libpython3.12-minimal_3.12.3-1ubuntu0.4_amd64.deb"
RUN apt install -y "./python3.12-minimal_3.12.3-1ubuntu0.4_amd64.deb"
RUN apt install -y "./libpython3.12-stdlib_3.12.3-1ubuntu0.4_amd64.deb"
RUN apt install -y "./libpython3.12t64_3.12.3-1ubuntu0.4_amd64.deb"
RUN apt install -y "./python3.12_3.12.3-1ubuntu0.4_amd64.deb"
RUN apt download python3-pip && dpkg --force-all -i python3-pip*.deb
RUN python3.12 -m pip install --break-system-packages "fastapi[standard]"

RUN echo "INS{FakeFlag!}" > /flag.txt
 
USER u-insotransfer:g-insotransfer
COPY ./app /app

WORKDIR /app

EXPOSE 8000
CMD ["fastapi", "run", "main.py", "--workers", "50", "--proxy-headers"]
