# ABOUTME: Makefile for EKS monitoring stack build, validation, and deployment.
# ABOUTME: Provides targets for rendering Kustomize manifests, linting, diffing, and applying.

.PHONY: build validate diff apply start stop clean cdk-synth cdk-deploy help

SHELL := /bin/bash
ENV ?= staging
BUILD_DIR := build/$(ENV)

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Render all kustomize manifests (ENV=staging|prod)
	@echo "Building manifests for $(ENV)..."
	@mkdir -p $(BUILD_DIR)
	@kustomize build --enable-helm clusters/eks-$(ENV) -o $(BUILD_DIR)/
	@echo "Manifests written to $(BUILD_DIR)/"

validate: build ## Lint rendered manifests with kubeconform
	@echo "Validating $(ENV) manifests..."
	@if command -v kubeconform >/dev/null 2>&1; then \
		find $(BUILD_DIR) -name '*.yaml' -o -name '*.yml' | \
			xargs kubeconform -strict -ignore-missing-schemas \
				-schema-location default \
				-schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
				-summary; \
	else \
		echo "kubeconform not found — skipping validation (install: go install github.com/yannh/kubeconform/cmd/kubeconform@latest)"; \
	fi

diff: build ## Preview changes against live cluster (ENV=staging|prod)
	@echo "Diffing $(ENV) manifests against live cluster..."
	@kubectl diff -f $(BUILD_DIR)/ || true

apply: build ## Apply manifests to cluster (ENV=staging|prod)
	@echo "Applying $(ENV) manifests..."
	@kubectl apply -f $(BUILD_DIR)/ --server-side
	@echo "Applied to $(ENV)."

start: ## Alias for apply ENV=staging
	@$(MAKE) apply ENV=staging

stop: ## Delete the monitoring stack from staging
	@echo "Deleting monitoring stack from staging..."
	@kubectl delete -f build/staging/ --ignore-not-found || true

clean: ## Remove build artifacts
	@rm -rf build/

cdk-synth: ## Synthesize CDK CloudFormation templates
	@cd cdk && cdk synth

cdk-deploy: ## Deploy CDK stack (ENV=staging|prod)
	@cd cdk && cdk deploy monitoring-$(ENV)
