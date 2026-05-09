FROM rust:1.88.0-slim as builder
WORKDIR /usr/src/rust-api

RUN apt-get update && apt-get install -y pkg-config libssl-dev && rm -rf /var/lib/apt/lists/*

COPY Cargo.toml .
RUN mkdir src
RUN echo 'fn main() { println!("cargo fetch placeholder"); }' > src/main.rs
RUN cargo fetch

COPY . .
RUN cargo install --path .

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/cargo/bin/rust_api /usr/local/bin/rust_api
EXPOSE 5000
CMD ["rust_api"]
