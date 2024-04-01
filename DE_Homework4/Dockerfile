FROM python:3.11

WORKDIR /code

RUN apt-get update
RUN pip install --upgrade pip

COPY . /code
RUN pip install -r requirements.txt

CMD ["python", "main.py"]