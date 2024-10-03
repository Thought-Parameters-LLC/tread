# Installation of Tread

## Installing using Kustomize

For basic installation, run the following command:

```bash
kubectl apply -f ./kubernetes/manifest/base
```

## Installing using Helm

Package Helm file first

```bash
helm package ./kubernetes/helm/
```

For cpu-only pod

```bash
helm install tread ./tread-*.tgz
```

Check the `kubernetes/helm/values.yaml` file to know which parameters are available for customization.
