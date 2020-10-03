FROM python:3.8.6-buster

LABEL maintainer="ferry.de.boer@gmail.com"

# Install pipx to help installing pipenv as command line tool.
RUN pip install pipenv

ENV PROJECT_DIR /usr/local/src/api

WORKDIR ${PROJECT_DIR}

# Not neeeded in development.
# COPY jomai ${PROJECT_DIR}/jomai
COPY Pipfile* ${PROJECT_DIR}/
COPY setup.cfg ${PROJECT_DIR}

RUN pipenv install --system --deploy

EXPOSE 8000

#CMD ["sh"]
ENTRYPOINT ["uvicorn", "jomai.main:app"]