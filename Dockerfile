FROM python:3.8

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
WORKDIR ./csi_be
CMD ['python3' 'run.py']
