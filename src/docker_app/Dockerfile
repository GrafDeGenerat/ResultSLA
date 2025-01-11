FROM postgres:14-alpine
LABEL authors="Denis Strekalev"
ENV POSTGRES_PASSWORD=postgres_pass
ENV POSTGRES_DB=empty
COPY psql_init.sql /docker-entrypoint-initdb.d/psql_init.sql
EXPOSE 5432
CMD [ "postgres" ]