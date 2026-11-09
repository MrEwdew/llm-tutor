FROM python:3.13-slim@sha256:ae14d4ce8771606477a81446e7ef429edd6762305fc50c84507c1041fa8285d1
RUN pip install --no-cache-dir wypp==2.3.0 typing_extensions==4.15.0
RUN python -B -c "import wypp; from typing_extensions import is_typeddict"
WORKDIR /work
USER 10001:10001
