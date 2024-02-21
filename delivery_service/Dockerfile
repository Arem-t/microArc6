FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

COPY ./delivery_service /code

COPY ./delivery_service/test.db /code/test.db

EXPOSE 80

CMD ["uvicorn", "delivery_service:app", "--host", "127.0.0.1", "--port", "8080" ]