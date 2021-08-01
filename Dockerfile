FROM python:3

WORKDIR /usr/src/app

COPY pyproject.toml ./
COPY poetry.lock ./
RUN pip install 'poetry==1.1.7'
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .