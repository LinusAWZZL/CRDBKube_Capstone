CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replication_slot1');
SELECT pg_create_physical_replication_slot('replication_slot2');
SELECT pg_create_physical_replication_slot('replication_slot3');
