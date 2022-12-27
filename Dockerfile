FROM python:3.11-alpine

WORKDIR /opt/action

COPY LICENSE README.md requirements.txt src/post.py src/constansts/py ./

RUN pip install -U pip && pip install -r requirements.txt

ENTRYPOINT ["/opt/action/post.py"]