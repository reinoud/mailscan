FROM python:3.7-alpine

WORKDIR /usr/src/app

# Copy necessary files
COPY rocketload rocketload
COPY requirements.txt .
COPY setup.py .

# Install python depedencies
RUN apk add --no-cache build-base \
    && pip install -r requirements.txt \
    && pip install . \
    && ln -s $(which rocketload) rocketload-executable \
    # Uninstall build-base for image size
    && apk del build-base

CMD python -u rocketload-executable