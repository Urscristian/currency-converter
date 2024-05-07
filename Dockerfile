FROM python:3.9-slim

STOPSIGNAL SIGQUIT

RUN pip install pipenv

COPY Pipfile* ./
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt

CMD ["gunicorn", "--preload", "-b", "0.0.0.0:8020", "project.wsgi:application", "--threads", "8", "-w", "4"]
