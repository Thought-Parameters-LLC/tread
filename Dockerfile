ARG USE_OLLAMA=false

ARG USE_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
ARG USE_RERANKING_MODEL=""
ARG BUILD_HASH=dev-build
ARG UID=0
ARG GID=0

FROM --platform=$BUILDPLATFORM node:21-alpine3.19 as build
ARG BUILD_HASH

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
ENV APP_BUILD_HASH=$BUILD_HASH
RUN npm run build

FROM python:3.11-slim-bookworm as base

ARG UID=0
ARG GID=0

ARG SECRET_KEY=""

## Basis ##
ENV ENV=production \
  PORT=7080 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  TPNEWSLETTER_SECRET_KEY=${SECRET_KEY:-"$(openssl rand -hex 32)"}

WORKDIR /app/backend

ENV HOME /root

# Create user and group if not root
RUN if [ $UID -ne 0 ]; then \
    if [ $GID -ne 0 ]; then \
    addgroup --gid $GID app; \
    fi; \
    adduser --uid $UID --gid $GID --home $HOME --disabled-password --no-create-home app; \
    fi

RUN chown -R $UID:$GID /app $HOME

COPY --chown=$UID:$GID ./backend/requirements.txt ./requirements.txt

RUN apt-get update && \
  apt-get install -y --no-install-recommends git build-essential pandoc netcat-openbsd curl && \
  apt-get install -y --no-install-recommends gcc python3-dev && \
  apt-get install -y --no-install-recommends curl jq && \
  # clean up
  rm -rf /var/lib/apt/lists/*

RUN pip3 install uv && \
  uv pip install --system -r requirements.txt --no-cache-dir && \
  chown -R $UID:$GID /app/backend/data

  # copy built frontend files
  COPY --chown=$UID:$GID --from=build /app/build /app/build
  COPY --chown=$UID:$GID --from=build /app/CHANGELOG.md /app/CHANGELOG.md
  COPY --chown=$UID:$GID --from=build /app/package.json /app/package.json

  # copy backend files
COPY --chown=$UID:$GID ./backend .

EXPOSE 7080

HEALTHCHECK CMD curl --silent --fail http://localhost:${PORT:-7080}/health | jq -ne 'input.status == true' || exit 1

USER $UID:$GID

ARG BUILD_HASH
ENV BACKEND_BUILD_VERSION=${BUILD_HASH}
ENV DOCKER true

CMD [ "bash", "start.sh" ]
