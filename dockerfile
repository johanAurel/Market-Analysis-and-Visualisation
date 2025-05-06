# Dockerfile for Jenkins agent with Docker CLI
FROM jenkins/inbound-agent:latest

USER root

RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean

USER jenkins
