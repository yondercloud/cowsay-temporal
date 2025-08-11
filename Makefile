.PHONY: build push help

IMAGE_NAME := lhitchon/cowsay-temporal
PLATFORM := linux/amd64

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

build: ## Build the Docker image for linux/amd64 platform
	docker build --platform $(PLATFORM) -t $(IMAGE_NAME) .

push: ## Push the Docker image to Docker Hub
	docker push $(IMAGE_NAME)

build-push: build push ## Build and push the Docker image

restart-api: ## Restart the deployed api
	kubectl rollout restart deployment/cowsay-api

run-worker: ## Run the worker in Docker locally
	docker run -it --rm \
		-e TEMPORAL_HOST=host.docker.internal:7233 \
		$(IMAGE_NAME) --mode worker

run-api: ## Run the api in Docker locally
	docker run -it --rm \
		-e TEMPORAL_HOST=host.docker.internal:7233 \
		-p 8000:8000 \
		$(IMAGE_NAME) --mode api

restart-worker: ## Restart the deployed worker
	kubectl rollout restart deployment/cowsay-worker
