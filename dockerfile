FROM python:3.10-buster

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    xz-utils \
    fontconfig \
    libjpeg62-turbo \
    libxrender1 \
    xfonts-75dpi \ 
    xfonts-base \
    libxrender1\
    libfontconfig1\
    libjpeg62-turbo\
    fontconfig \
    libfreetype6 \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxrender-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    libx11-dev \
    libxcb1-dev \
    libxext-dev \
    libxrandr-dev \
    libssl-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    wkhtmltopdf

ARG PORT_BUILD=8000
ENV PORT=$PORT_BUILD

COPY requeriments.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requeriments.txt

COPY . .

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 insert_banco.py

EXPOSE $PORT
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]