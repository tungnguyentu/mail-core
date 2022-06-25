FROM python:3.8
WORKDIR /usr/mail-core
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8888
CMD ["python", "main.py"]