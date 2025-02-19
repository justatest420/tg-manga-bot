# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade pip, setuptools, and wheel
RUN python -m pip install --upgrade pip setuptools wheel

# Copy requirements file
COPY requirements.txt .

RUN python -m pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY . /app

#RUN alembic upgrade head

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["bash", "start.sh"]
