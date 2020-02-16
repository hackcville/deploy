FROM python:3.8.0-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# install psycopg2 dependencies
RUN apk update \
  && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /app/
RUN pip install -r requirements.txt

# copy the rest of the app
COPY . .

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]