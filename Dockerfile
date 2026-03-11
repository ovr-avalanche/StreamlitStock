# 1. use a base image
FROM python:3.12-slim 

# 2. install uv / replace with current verion of uv (uv --version)
COPY --from=ghcr.io/astral-sh/uv:0.9.24 /uv /uvx /bin/

# 3. Set the dir inside the container
WORKDIR /app

# 3.5. Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# 4.  Copy Only dependency files ("Cache Layer")
COPY pyproject.toml uv.lock ./

# 5. instead of pip install -r requirements.txt
# --frozen             | ignores.tompl and uses only uv.lock
# --no-install-project | dont look for the src folder yet ?
# --no-dev             | leave out development dependencies (tools only used in development)
# 
# --locked             | looks for uv.lock, but updates it if there are changes in pyproject.toml (?)
RUN uv sync --frozen --no-install-project --no-dev


# 6. Copy the rest (src/, data/, etc.)
COPY . . 

# 7. Sync again to install the project itself
RUN uv sync --frozen --no-dev

# 8. add the uv virtual env to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# 9. Expose the Streamlit default port
EXPOSE 8501

# 10. Entrypoint 
ENTRYPOINT [ "streamlit", "run", "src/StreamlitStock.py", "--server.port=8501", "--server.address=0.0.0.0" ]