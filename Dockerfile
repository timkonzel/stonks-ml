FROM python:3.8.3

RUN pip install tensorflow
RUN pip install finnhub-python

WORKDIR /srv

COPY . /srv/

CMD ["python", "bootstrapper.py"]