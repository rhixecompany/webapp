# As Scrapy runs on Python, I choose the official Python 3 Docker image.
FROM python:3.10-alpine3.16
ENV PYTHONUNBUFFERED=1

# Set the working directory to /usr/src/app.
WORKDIR /home/backend/image_downloader
COPY ../requirements.txt ./

RUN apk add --upgrade --no-cache build-base linux-headers && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the project source code from the local host to the filesystem of the container at the working directory.
COPY . .

# Run the crawler when the container launches.
CMD [ "python3", "manage.py downloads" ]