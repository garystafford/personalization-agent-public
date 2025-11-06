# linux/amd64 version for ECS: https://github.com/astral-sh/uv/pkgs/container/uv/520833613?tag=python3.13-bookworm-slim
FROM ghcr.io/astral-sh/uv:0.8.19-python3.13-bookworm-slim@sha256:b0424921960714b48b03b2ffca6165e2e339bcccc25cfac0c5cc492bddf70d15

# Create a non-root user named 'appuser'
RUN useradd -m appuser

# Set the working directory for the user
WORKDIR /home/appuser

# Configure UV for container environment
ENV UV_SYSTEM_PYTHON=1 UV_COMPILE_BYTECODE=1

# Install from requirements file
COPY requirements.txt requirements.txt
RUN uv pip install --no-cache-dir -r requirements.txt -U

# Set AWS region environment variable
ENV AWS_REGION=us-east-1

# Model configuration environment variables
ENV MODEL_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0
ENV MODEL_TEMPERATURE=0.2
ENV BYPASS_TOOL_CONSENT=True

# Signal that this is running in Docker for host binding logic
ENV DOCKER_CONTAINER=1

# Expose the port for Gradio
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Copy entire project (respecting .dockerignore)
COPY . .

# # Ensure the user profiles are writable
RUN chmod -R 666 /home/appuser/viewer_profiles.json

# Switch to the 'appuser' for subsequent instructions and container runtime
USER appuser

# Add the health check instruction
# HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
# CMD curl --fail http://localhost:7860 || exit 1

# Run the application
CMD ["python", "app.py"]