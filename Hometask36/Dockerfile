FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

WORKDIR /app

RUN apt-get update
RUN pip install --upgrade pip

COPY . /app
RUN pip install -r requirements.txt --default-timeout=100

EXPOSE 7000
CMD ["python", "demo.py"]