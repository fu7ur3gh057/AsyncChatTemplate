FROM python:3.10.9-bullseye
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create and set workdir
WORKDIR /app/backend


RUN pip install --upgrade pip
COPY ./requirements.txt /app/backend/requirements.txt

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy local project
COPY .. .
# make our worker-entrypoint.sh executable
RUN chmod +x ./deploy/scripts/worker-entrypoint.sh
# execute our worker-entrypoint.sh file
ENTRYPOINT ["./deploy/scripts/worker-entrypoint.sh"]