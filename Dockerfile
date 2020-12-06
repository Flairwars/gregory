FROM python:3
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./src /app/src
RUN chmod +x ./app/src/main.py
CMD [ "python", "./app/src/main.py"]