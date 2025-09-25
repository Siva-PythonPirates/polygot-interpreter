FROM python:3.9-slim
WORKDIR /usr/src/app
COPY script.py .
# Use ENTRYPOINT to set the executable
ENTRYPOINT ["python", "script.py"]