FROM python:3.7-alpine

WORKDIR /usr/src/app

# Copy necessary files
COPY mailscan mailscan
COPY requirements.txt .
COPY setup.py .

# Install python depedencies
RUN apk add --no-cache build-base \
    && pip install -r requirements.txt \
    && pip install . \
    && ln -s $(which mailscan) mailscan-executable \
    # Uninstall build-base for image size
    && apk del build-base

CMD python -u mailscan-executable