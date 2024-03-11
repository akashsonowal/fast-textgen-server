# llama2-server

Setup Minikube Cluster
```
minikube start --memory=14978 --cpus=4 --force
```
Run Docker with GPU access (use Nvidia Container Toolkit)
```
docker run --rm --runtime=nvidia --gpus all llama2-server:v1
```

Run locally
```
python3 entrypoint.py
```
