CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replication_slot1');
SELECT pg_create_physical_replication_slot('replication_slot2');
SELECT pg_create_physical_replication_slot('replication_slot3');

CREATE USER postgres_exporter WITH PASSWORD 'password';
ALTER USER postgres_exporter SET SEARCH_PATH TO postgres_exporter,pg_catalog;
GRANT CONNECT ON DATABASE defaultdb TO postgres_exporter;
GRANT USAGE ON SCHEMA pg_catalog TO postgres_exporter;
GRANT SELECT ON ALL TABLES IN SCHEMA pg_catalog TO postgres_exporter;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA pg_catalog TO postgres_exporter;
