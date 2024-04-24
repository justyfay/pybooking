FROM python:3.12 as python-base

WORKDIR /pybooking

COPY /pyproject.toml /pybooking

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

RUN chmod a+x /pybooking/docker/*.sh