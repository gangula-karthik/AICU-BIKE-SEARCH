# start by pulling the python image
FROM python:3.9.16-slim-buster

# switch working directory
WORKDIR /app

COPY ./app/requirements.txt .

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY ./app .

EXPOSE 80

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py"]

