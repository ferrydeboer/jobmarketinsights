FROM python:3.8.6-buster

LABEL maintainer="ferry.de.boer@gmail.com"

# Install pipx to help installing pipenv as command line tool.
RUN pip install pipenv

ENV PROJECT_DIR /usr/local/src/api

# Not needed in development.
# COPY jomai ${PROJECT_DIR}/jomai
COPY Pipfile* ${PROJECT_DIR}/
COPY setup.cfg ${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}

# Allow installing dev dependencies to run tests
ARG DEBUG=false
RUN bash -c "if [ $DEBUG == 'true' ] ; then pipenv install --system --dev ; else pipenv install --system --deploy; fi"

EXPOSE 8000

CMD ["sh", "-c", "tail -f /dev/null"]
#ENTRYPOINT ["uvicorn", "jomai.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
#CMD ["python", "jomai/main.py"]