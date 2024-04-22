FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN python3 -m pip install --upgrade pip &&\
    python3 -m pip install pipx &&\
    python3 -m pipx ensurepath &&\
    /bin/bash -c "source /root/.bashrc" &&\
    PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install poetry


COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    pipx install poetry && \
    poetry install --no-dev --no-interaction --no-ansi

COPY . .

RUN poetry install --no-dev --no-interaction --no-ansi

# CMD ["poetry", "run", "streamlit", "run", "src/insurance_gpt/app/1. InsuranceGPT Chat.py"]
