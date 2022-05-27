FROM python:3.7

RUN apt-get update
RUN apt-get install -y ffmpeg

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]