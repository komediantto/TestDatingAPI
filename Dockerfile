FROM python:3

RUN mkdir /api

COPY ./ /api
RUN pip3 install -r /api/requirements.txt --no-cache-dir
WORKDIR /api/app
RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0:8000"]
