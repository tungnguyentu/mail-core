FROM python:3.8-slim
WORKDIR /usr/mail-core
RUN apt update && apt-get install -y default-libmysqlclient-dev build-essential
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8888
CMD ["python", "main.py"]
