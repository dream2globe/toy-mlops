FROM python:3.8

WORKDIR /usr/src/app/
COPY . /usr/src/app/

ENV PYTHONPATH = /usr/src/app
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /usr/src/app/requirements.txt

EXPOSE 9009

CMD ["uvicorn", "app_serving.serving:app", "--host=0.0.0.0", "--port=9009"]