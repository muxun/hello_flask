FROM python:3.6.0-alpine
RUN pip install --upgrade pip && pip install Flask
WORKDIR /hello
COPY . /hello
CMD ["python3","hello.py"]
