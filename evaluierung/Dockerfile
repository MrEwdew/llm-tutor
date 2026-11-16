FROM python:3.13-slim@sha256:ae14d4ce8771606477a81446e7ef429edd6762305fc50c84507c1041fa8285d1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git unzip ripgrep libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

ARG OPENCODE_VERSION=2.3.0
ARG OPENCODE_URL=https://registry.npmjs.org/@opencode/cli-linux-x64/-/cli-linux-x64-2.3.0.tgz
RUN curl --fail --location --proto '=https' --tlsv1.2 "$OPENCODE_URL" -o /tmp/opencode.tar.gz \
    && python -c "import base64,hashlib,pathlib; actual=base64.b64encode(hashlib.sha512(pathlib.Path('/tmp/opencode.tar.gz').read_bytes()).digest()).decode(); assert actual == '8T3K8L6Nd4fSG5BSgofqhmIDQ1ZvzDZZ2J7bFVB9RK1d5Hjqh24IcxgbcwpgGKkdvItrayi4Rl+wrSmhl17FFg==', 'OpenCode archive checksum mismatch'" \
    && mkdir /tmp/opencode \
    && tar -xzf /tmp/opencode.tar.gz -C /tmp/opencode \
    && install -m 755 "$(find /tmp/opencode -type f -name opencode -print -quit)" /usr/local/bin/opencode \
    && test "$(opencode --version | awk '{print $NF}' | sed 's/^v//')" = "$OPENCODE_VERSION" \
    && mkdir -p /opt/evaluation \
    && sha256sum /usr/local/bin/opencode > /opt/evaluation/opencode.sha256 \
    && rm -rf /tmp/opencode /tmp/opencode.tar.gz

COPY requirements.txt /opt/evaluation/requirements.txt
RUN pip install --no-cache-dir -r /opt/evaluation/requirements.txt \
    && python -m pip check \
    && python -c "import wypp, pypdf, deepagents; from deepagents.backends import LocalShellBackend" \
    && pip freeze > /opt/evaluation/python-packages.txt \
    && dpkg-query -W > /opt/evaluation/system-packages.txt

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/tmp/home \
    XDG_CONFIG_HOME=/tmp/config \
    XDG_DATA_HOME=/tmp/data \
    XDG_CACHE_HOME=/tmp/cache \
    XDG_STATE_HOME=/tmp/state \
    EVALUATION_CONTAINER=1

WORKDIR /work
USER 10001:10001
