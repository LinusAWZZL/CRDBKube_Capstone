# Postgreslq Set Up

# Requirements
Docker
psql
pgpool

## Database set up
On primary Node
```
docker compose -f docker-master.yaml up
```
then load pgpool with pgpool.conf and pool_passwd

On replica Nodes
```
docker compose -f docker-replica.yaml up
```

