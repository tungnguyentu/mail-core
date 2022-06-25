FROM python:3.8
WORKDIR /usr/mail-core
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]