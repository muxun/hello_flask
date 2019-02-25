FROM python:3.6.0-alpine
RUN pip install --upgrade pip && pip install Flask
WORKDIR /router
COPY . /router
CMD ["python3","router.py"]
