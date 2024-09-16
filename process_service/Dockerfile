
FROM python:3.9


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./* /code/app/


CMD ["fastapi", "run", "app/api.py", "--port", "5000", "--workers", "4", "--host", "0.0.0.0"]