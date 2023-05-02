# pull official base image
FROM python:3.10.7

# RUN apt-get update && apt-get install -y redis-server
# RUN redis-server --daemonize yes
# RUN redis-cli ping
RUN pip install poetry
WORKDIR /app
COPY . .
EXPOSE 8000
STOPSIGNAL SIGTERM
RUN poetry config virtualenvs.in-project true
RUN poetry install
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]