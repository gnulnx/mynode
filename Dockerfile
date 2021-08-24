FROM python:3.8

WORKDIR /app

# Copy just the requirements.txt first to leverage Docker cache
COPY ./requirements* /app/requirements.txt
RUN python3.8 -m pip install pip --upgrade --force
RUN pip3.8 install -r requirements.txt

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY server.py /app/server.py
ENTRYPOINT ["./entrypoint.sh"]

