FROM python:3.9-slim

# Faqat kerakli tizim kutubxonalarini o‘rnatamiz
RUN apt-get update && \
    apt-get install -y build-essential libatlas-base-dev && \
    apt-get clean

# Python kutubxonalarni o‘rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bot fayllarini konteynerga yuklash
COPY . /app
WORKDIR /app

# Botni ishga tushirish
CMD ["python", "main.py"]
