helm install crdb cockroachdb/cockroachdb \
  --set fullnameOverride=crdb \
  --set single-node=true \
  --set statefulset.replicas=1 \
  --set tls.enable=false \ 
  --debug