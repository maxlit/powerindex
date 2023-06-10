FROM jupyter/minimal-notebook
COPY requirements.txt requirements.txt
# Clone a repository (my website in this case)
RUN git clone https://gitlab.com/maxlit/powerindex.git
RUN cd powerindex

#RUN pip3 install -r requirements.txt
ENV POETRY_VERSION=1.2.2
#ENV POETRY_HOME=/opt/poetry
#ENV POETRY_VENV=/opt/poetry-venv
#ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
#RUN python3 -m venv $POETRY_VENV
RUN pip install -U pip setuptools
RUN pip install poetry==${POETRY_VERSION}

# Copy and install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi
