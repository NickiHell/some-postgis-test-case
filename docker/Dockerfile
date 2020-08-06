FROM python:3

ENV PROJECT_ROOT=/app
ENV PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

RUN mkdir $PROJECT_ROOT/

COPY ./Pipfile ./Pipfile.lock $PROJECT_ROOT/
WORKDIR $PROJECT_ROOT

RUN pip install --upgrade wheel pip pipenv
RUN pipenv install

COPY ./src $PROJECT_ROOT

ENTRYPOINT ["pipenv", "run"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${UVICORN_PORT}"]
