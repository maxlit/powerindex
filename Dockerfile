# Use a specific base image version from quay.io
FROM quay.io/jupyter/minimal-notebook:x86_64-python-3.11.7

# Set the working directory in the container to /app
WORKDIR /app

# Copy the pyproject.toml and uv.lock files into the container at /app
COPY pyproject.toml uv.lock /app/

# Install uv and install dependencies
RUN pip install --progress-bar off uv && \
    uv sync --no-dev

# Copy the contents of the pyEdgeworthBox repository into the container
COPY . /app/

#RUN pip install --progress-bar off twine && python setup.py sdist bdist_wheel


# Continue with any other commands you need
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token="]