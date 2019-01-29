FROM python:3.6.0
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY python-lib/ /code/python-lib/
COPY built_env.py /code/
COPY requirements.txt /code/
# RUN pip install -r /code/requirements.txt
RUN python /code/built_env.py

ADD . /code/
ENV DJANGO_RUN_ENV TEST

EXPOSE 8000
