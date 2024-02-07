FROM python:3.11-slim-bullseye
RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get install -y gcc default-libmysqlclient-dev pkg-config -y
WORKDIR /app/acbo
COPY /acbo/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY /acbo /app/acbo

RUN rm -f /app/requirements.txt /app/acbo/requirements.txt 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
