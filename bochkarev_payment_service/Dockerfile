FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

COPY ./bochkarev_payment_service /code

COPY ./bochkarev_payment_service/payment.db /code/payment.db

EXPOSE 8080

CMD ["python", "bochkarev_payment_service.py"]