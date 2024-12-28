# CockroachDB Set Up

# Requirements
Kubernetes
Helm

## Additional Node for Admin Account registration

## Database set up

```
kubectl -n linus run cockroachdb-client -it --image=cockroachdb/cockroach:v23.1.8 --rm --restart=Never -- sql --insecure --host=crdb4-public
```

```
CREATE USER linus;
GRANT admin TO linus;
```

Once Done if hang:
kubectl delete cockroachdb-client -n linus

## Booting

## Port forward

### CRDB Cluster
kubectl port-forward pod/crdb4-0 26256:26257 -n linus
kubectl port-forward svc/crdb4-public 8084:8080 -n linus

## Temp notes
PV set storageclass manual
Pods PVC template storageclass manual
Run Jobs init
add tolerance for taint