# Mental Health Chatbot — Student MVP

This is a minimal, end-to-end scaffold to help you learn and demo: FastAPI, Docker, Jenkins, Prometheus/Grafana, Kubernetes, and Terraform.

## 1) Run locally (no Docker)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```
Open `web/index.html` in your browser and chat. (It calls `http://localhost:8000/chat`.)

## 2) Run with Docker
```bash
cd infra
docker build -t mhb:local -f Dockerfile ..
docker run -p 8000:8000 mhb:local
```
Visit the same `web/index.html` (or curl `localhost:8000/healthz`).

## 3) Run the full stack with docker-compose (API + Prometheus + Grafana)
```bash
cd infra
docker compose up -d
```
- API: `http://localhost:8000`
- Metrics: `http://localhost:8000/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (user: admin, pass: admin)

## 4) Jenkins (simple pipeline)
1. Create Jenkins credential `dockerhub-creds` (username/password).
2. Use the provided `ci/Jenkinsfile`.
3. Stages: checkout → test → build image → (optional) scan → push → deploy (compose).

## 5) Kubernetes (manifests)
- Replace `<REPLACE_WITH_YOUR_IMAGE>` in `k8s/deployment.yaml` with the image you pushed (e.g., `docker.io/you/mhb-api:1`).
- Apply:
```bash
kubectl apply -f k8s/01-namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
# In cloud with ALB controller:
kubectl apply -f k8s/ingress.yaml
```
- Port forward for local testing:
```bash
kubectl -n mhb port-forward svc/mhb-api 8080:80
```
Then open `http://localhost:8080/healthz`.

## 6) Terraform (skeleton for you to extend)
This just creates an S3 bucket to prove TF works. Extend with modules for VPC/EKS/RDS when ready.
```bash
cd terraform
terraform init
terraform apply
```

## 7) Project structure
```
backend/        # FastAPI app + simple mood/crisis logic
web/            # Static HTML chat client
infra/          # Dockerfile + docker-compose + Prometheus config
k8s/            # K8s manifests (Deployment, Service, HPA, Ingress)
ci/             # Jenkinsfile
terraform/      # Terraform skeleton
```

## 8) Notes
- This bot is **not** a medical device. It only provides generic coping tips and crisis routing.
- Do not log sensitive data. If you must store, anonymize and secure it.
```