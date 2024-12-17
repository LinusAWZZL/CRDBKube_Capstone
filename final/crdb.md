# CockroachDB Set Up

# Requirements
Kubernetes
Helm

## Additional Node for Admin Account registration

## Database set up

Once Done:
kubectl delete -f client-secure1.yaml

## Booting

## Port forward

### CRDB Single
kubectl port-forward pod/crdb1-0 26257:26257
kubectl port-forward svc/crdb1-public 8085:8080

### CRDB Cluster
kubectl port-forward pod/crdb4-0 26256:26257
kubectl port-forward svc/crdb4-public 8084:8080

## Temp notes
PV set storageclass manual
Pods PVC template storageclass manual
Run Jobs init
add tolerance for taint