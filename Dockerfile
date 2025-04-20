
# 1. Python 3.9 asosida imijni tanlaymiz
FROM python:3.9-slim

# 2. Kerakli tizim kutubxonalarini o'rnatamiz
RUN apt-get update && \
    apt-get install -y build-essential wget libffi-dev libatlas-base-dev && \
    apt-get clean

# 3. TA-Lib C kutubxonasini yuklab olish va o'rnatish
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && make && make install && \
    cd .. && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# 4. TA-Lib kutubxonasini tan olish uchun
ENV LD_LIBRARY_PATH=/usr/lib

# 5. Python kutubxonalarni o'rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Ilova fayllarini konteynerga ko‘chirish
COPY . /app
WORKDIR /app

# 7. Botni ishga tushirish
CMD ["python", "main.py"]
