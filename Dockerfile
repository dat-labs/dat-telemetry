FROM python:3.10
WORKDIR /repo

COPY . .
RUN pip install poetry

# RUN poetry add 'uvicorn[standard]'
RUN poetry config virtualenvs.create false && poetry lock && poetry install --no-root


# RUN pip install -e .
# CMD python -m http.server
CMD celery -A src.main worker -Q dat-telemetry-q