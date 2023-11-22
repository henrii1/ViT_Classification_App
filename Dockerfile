FROM python:3.12

COPY ./requirements.txt /mainapp/requirements.txt

WORKDIR /mainapp

RUN pip install -r requirements.txt

COPY mainapp/* /mainapp

COPY ./examples /webapp/examples

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]