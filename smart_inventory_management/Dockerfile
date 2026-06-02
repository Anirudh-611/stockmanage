FROM python:3.14

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD ["gunicorn","smart_inventory_management.wsgi:application","--bind","0.0.0.0:10000"]
