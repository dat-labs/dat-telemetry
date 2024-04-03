FROM python:3.10
WORKDIR /repo
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/ && echo "${SSH_PRIVATE_KEY}" >> /root/.ssh/id_rsa
RUN chmod 400 /root/.ssh/id_rsa && ssh-keyscan github.com >> /root/.ssh/known_hosts

COPY pyproject.toml .
COPY poetry.lock .
RUN pip install poetry

# RUN poetry add 'uvicorn[standard]'
RUN poetry config virtualenvs.create false && poetry lock && poetry install --no-root


# RUN pip install -e .
# CMD python -m http.server
CMD celery -A src.main worker -Q dat-telemetry-q