FROM python:3.12
COPY server.py /server.py
COPY requirements.txt /tmp/requirements.txt
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

ENTRYPOINT ["python3","/server.py"]
