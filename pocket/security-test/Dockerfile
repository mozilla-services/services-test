# SEE https://github.com/zaproxy/zaproxy/issues/1880#issuecomment-142677598

FROM owasp/zap2docker-stable
MAINTAINER grunny

RUN pip install --upgrade git+https://github.com/Grunny/zap-cli.git

RUN chown -R zap /zap/
ENV ZAP_PORT 8080
