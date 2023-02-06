# syntax=docker/dockerfile:1
FROM node:16-slim as base
FROM base as builder

RUN <<EOT
    apt-get update
    buildDeps="python3 build-essential git ca-certificates"
    apt-get install -y --no-install-recommends $buildDeps
    rm -rf /var/lib/apt/lists/*
EOT

COPY --chown=node . /build/
RUN corepack enable

USER node
WORKDIR /build
RUN <<EOT
    make install
    yarn build
EOT

FROM base

LABEL maintainer="Benoît Suttor <benoit@suttor.be>" \
      org.label-schema.name="oality-website-frontend" \
      org.label-schema.description="Oality Website frontend image." \
      org.label-schema.vendor="Benoît Suttor"

RUN apt-get update
RUN apt-get install -y --no-install-recommends busybox
RUN busybox --install -s
RUN rm -rf /var/lib/apt/lists/*



USER node
COPY --from=builder /build/ /app/

WORKDIR /app
EXPOSE 3000
CMD ["yarn", "start:prod"]
