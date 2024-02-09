FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# / - root directory (c:\)
# WORKDIR /app -> mkdir /app && cd /app
WORKDIR /app

COPY requirements.txt /app/
# Result: /app/requirements.txt

RUN pip install -r requirements.txt

# COPY . /app/ # If we want to copy all files and directories
COPY apps /app/apps
COPY core /app/core
COPY nginx /app/nginx
COPY registry_office /app/registry_office
COPY static_files /app/static_files
COPY media_files /app/media_files
COPY templates /app/templates
COPY manage.py /app/