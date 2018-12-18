FROM python:3.6.0
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
# RUN pip install -r /code/requirements.txt
ADD . /code/
RUN python /code/built_env.py
ENV DJANGO_RUN_ENV TEST

EXPOSE 8000
