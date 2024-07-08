# CPU-bound worker example

Additional notes and improvement considerations are in [NOTES.md](NOTES.md) document. 

## Deployable services:

### API service

Exposes `POST /matrix-multiplication/submit-job/` endpoint that is an async endpoint whose only job is to publish a message on RabbitMQ.

### Worker service

A service that consumes messages from RabbitMQ and executes the work (matrix multiplication).

### Monitoring service

Exposes `/desired-worker-scale` endpoint that fetches `matrix-multiplication-worker` stats and calculates desired worker scale based on the number of messages in the queue

## Technologies

* Python 3.12
* FastAPI
* RabbitMQ
* Docker compose
* Kubernetes

## Local development

### Installation

Install Python 3.12.4 and poetry.

```shell
poetry env use 3.12.4
```

Inside `api`, `worker`, `monitoring`, and `load_test` directories run:

```shell
poetry install --with dev
```

### Activate virtual environment

```shell
poetry shell
```

### Run RabbitMQ locally

```shell
cd local
docker compose up -d
```

Uses `local/docker-compose.env` that mounts `local/rabbitmq` directory with all files required to configure RabbitMQ.


## Kubernetes deployment

### 1. Build Docker images

```shell
docker build -t cpu-bound-worker-api:1 ./api
docker build -t cpu-bound-worker-service:1 ./worker
docker build -t cpu-bound-worker-monitoring-api:1 ./monitoring
```

### 2. Install services

Sets up RabbitMQ, and three services: API, worker, and monitoring

```shell
kubectl apply -f ./k8s/config.yaml
```

### 3. Install HPA

HPA requires Prometheus. But I haven't been able to make Prometheus exporter node to work. I implemented the rest of the system as if it worked.

The role of prometheus is to export a metric that published through an API (monitoring API service).
The metric is consumed by `ServiceMonitor` resource that expose a K8s API that HPA can consume and use it to scale workers.

```shell
# Add Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add kube-prometheus-stack https://prometheus-community.github.io/helm-charts
helm repo add stable https://charts.helm.sh/stable
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace

# Install Prometheus Adapter
helm install prometheus-adapter prometheus-community/prometheus-adapter --namespace monitoring

helm install prometheus-operator prometheus-community/prometheus-community --namespace monitoring --create-namespace
```

### 4. Add monitoring services that supply data to HPA

```shell
helm upgrade --install prometheus-adapter prometheus-community/prometheus-adapter -f k8s/prometheus-adapter-values.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/worker-service-monitor.yaml
```

## Load testing

For the purposes of load testing I introduced an env. variable `SIMULATE_WORKLOAD_DURATION_IN_SEC`. The intention is to be used on the local development environment where putting the workstation under the significant load would render it unusable.
When we want to perform the real test, we change the payload in the test (make it configurable), and remove the environment variable from the worker deployment.

```shell
cd load_test
poetry shell
locust -f main.py -H http://127.0.0.1:8005 -r 2 -t 1m --headless
```

You can find additional options and flags using `locust` here: https://docs.locust.io/en/stable/index.html
