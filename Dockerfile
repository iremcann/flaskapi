FROM python:3.11.1
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY appfiles/ .
CMD [ "python", "./run.py" ]