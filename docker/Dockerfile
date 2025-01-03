FROM python:3.12-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG APP_HOME=/app

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential

WORKDIR ${APP_HOME}

COPY ./requirements.txt ./requirements.txt

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Gradio app (chatbot UI)
EXPOSE 8000
ENV GRADIO_SERVER_NAME="0.0.0.0"
