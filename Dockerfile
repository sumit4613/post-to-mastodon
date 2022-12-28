FROM python:3.11-alpine

WORKDIR /opt/action

COPY LICENSE README.md requirements.txt /opt/action/
ADD src /opt/action/src

RUN pip install -U pip && pip install -r requirements.txt

ENTRYPOINT ["python", "/opt/action/src/post.py"]