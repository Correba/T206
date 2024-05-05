FROM mysql:8.0
COPY custom.cnf /etc/mysql/conf.d/custom.cnf

ENV MYSQL_DATABASE=woody



COPY ./sql-scripts/ /docker-entrypoint-initdb.d/
