FROM grafana/grafana-enterprise

ENV GF_AUTH_DISABLE_LOGIN_FORM "true"
ENV GF_AUTH_ANONYMOUS_ENABLED "true"
ENV GF_AUTH_ANONYMOUS_ORG_ROLE "Admin"
ADD ./grafana.ini /etc/grafana/grafana.ini

ADD provisioning/dashboard/*.yml /etc/grafana/provisioning/dashboards/
ADD provisioning/datasource/*.yml  /etc/grafana/provisioning/datasources/
ADD provisioning/dashboard/*.json /var/lib/grafana/dashboards/