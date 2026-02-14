# Task Monitor Application - Makefile
# ===================================

# Variables
PYTHON := python3
VENV_DIR := app/venv
PIP := $(VENV_DIR)/bin/pip
PYTHON_VENV := $(VENV_DIR)/bin/python
REQUIREMENTS := app/requirements.txt
PORT := 5000

# Colors for output
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

##@ Setup Commands

.PHONY: setup
setup: ## 🚀 Complete project setup (create venv, install deps, create directories)
	@echo "$(BLUE)🚀 Setting up Task Monitor project...$(NC)"
	@$(MAKE) venv
	@$(MAKE) install
	@$(MAKE) directories
	@echo "$(GREEN)✅ Setup complete! Use 'make run' to start the dashboard.$(NC)"

.PHONY: venv
venv: ## 📦 Create virtual environment
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(BLUE)📦 Creating virtual environment...$(NC)"; \
		$(PYTHON) -m venv $(VENV_DIR); \
		echo "$(GREEN)✅ Virtual environment created!$(NC)"; \
	else \
		echo "$(YELLOW)⚡ Virtual environment already exists$(NC)"; \
	fi

.PHONY: install
install: venv ## 📥 Install/update dependencies
	@echo "$(BLUE)📥 Installing dependencies...$(NC)"
	@$(PIP) install --upgrade pip
	@$(PIP) install -r $(REQUIREMENTS)
	@echo "$(GREEN)✅ Dependencies installed!$(NC)"

.PHONY: directories
directories: ## 📁 Create necessary directories
	@echo "$(BLUE)📁 Creating necessary directories...$(NC)"
	@mkdir -p app/logs databag screenshots
	@echo "$(GREEN)✅ Directories created!$(NC)"

##@ Run Commands

.PHONY: run
run: setup ## 🌐 Start the web dashboard server
	@echo "$(BLUE)🌐 Starting Task Monitor Dashboard on http://localhost:$(PORT)$(NC)"
	@echo "$(YELLOW)   Press Ctrl+C to stop the server$(NC)"
	@echo ""
	@cd app && $(PYTHON_VENV) backend_server.py

.PHONY: dashboard
dashboard: run ## 🌐 Alias for 'make run' - start web dashboard

.PHONY: monitor
monitor: setup ## 🔄 Start continuous monitoring mode
	@echo "$(BLUE)🔄 Starting continuous monitoring...$(NC)"
	@$(PYTHON_VENV) run.py --monitor

.PHONY: snapshot
snapshot: setup ## 📷 Take a single performance snapshot
	@echo "$(BLUE)📷 Taking performance snapshot...$(NC)"
	@$(PYTHON_VENV) run.py --snapshot

.PHONY: monitor-limited
monitor-limited: setup ## 🔄 Start monitoring with custom process limit (usage: make monitor-limited LIMIT=10)
	@echo "$(BLUE)🔄 Starting monitoring with limit: $(or $(LIMIT),20)$(NC)"
	@$(PYTHON_VENV) run.py --monitor --limit $(or $(LIMIT),20)

##@ Development Commands

.PHONY: dev
dev: ## 🛠️ Development mode - install dev dependencies and run with auto-reload
	@echo "$(BLUE)🛠️ Setting up development environment...$(NC)"
	@$(PIP) install flask[dotenv] watchdog
	@echo "$(GREEN)✅ Dev dependencies installed! Starting in development mode...$(NC)"
	@cd app && FLASK_ENV=development FLASK_DEBUG=1 $(PYTHON_VENV) backend_server.py

.PHONY: test
test: setup ## 🧪 Run tests (if any test files exist)
	@echo "$(BLUE)🧪 Running tests...$(NC)"
	@if [ -d "tests" ] || ls test_*.py >/dev/null 2>&1 || ls app/test_*.py >/dev/null 2>&1; then \
		$(PYTHON_VENV) -m pytest -v; \
	else \
		echo "$(YELLOW)⚠️  No test files found. Create test_*.py files to add tests.$(NC)"; \
	fi

.PHONY: lint
lint: setup ## 🔍 Run code linting (requires flake8 to be installed)
	@echo "$(BLUE)🔍 Running linting...$(NC)"
	@if $(PYTHON_VENV) -c "import flake8" 2>/dev/null; then \
		$(PYTHON_VENV) -m flake8 --max-line-length=100 --exclude=$(VENV_DIR),__pycache__ .; \
	else \
		echo "$(YELLOW)⚠️  flake8 not installed. Install with: $(PIP) install flake8$(NC)"; \
	fi

.PHONY: format
format: setup ## ✨ Format code with black (requires black to be installed)
	@echo "$(BLUE)✨ Formatting code...$(NC)"
	@if $(PYTHON_VENV) -c "import black" 2>/dev/null; then \
		$(PYTHON_VENV) -m black --line-length=100 .; \
	else \
		echo "$(YELLOW)⚠️  black not installed. Install with: $(PIP) install black$(NC)"; \
	fi

##@ Data Commands

.PHONY: show-data
show-data: ## 📊 Display recent performance data
	@echo "$(BLUE)📊 Recent performance data:$(NC)"
	@if [ -f "databag/performance-monitoring.csv" ]; then \
		echo "$(GREEN) Performance Monitoring Data (last 10 entries):$(NC)"; \
		tail -n 10 databag/performance-monitoring.csv; \
		echo ""; \
	fi
	@if [ -f "databag/performance-snapshot.csv" ]; then \
		echo "$(GREEN) Performance Snapshot Data (last 10 entries):$(NC)"; \
		tail -n 10 databag/performance-snapshot.csv; \
	fi

.PHONY: backup-data
backup-data: ## 💾 Backup CSV data files
	@echo "$(BLUE)💾 Backing up data files...$(NC)"
	@mkdir -p backups
	@if [ -f "databag/performance-monitoring.csv" ]; then \
		cp databag/performance-monitoring.csv backups/performance-monitoring-$$(date +%Y%m%d-%H%M%S).csv; \
		echo "$(GREEN)✅ Monitoring data backed up$(NC)"; \
	fi
	@if [ -f "databag/performance-snapshot.csv" ]; then \
		cp databag/performance-snapshot.csv backups/performance-snapshot-$$(date +%Y%m%d-%H%M%S).csv; \
		echo "$(GREEN)✅ Snapshot data backed up$(NC)"; \
	fi

.PHONY: clear-data
clear-data: ## 🗑️ Clear CSV data files (with confirmation)
	@echo "$(YELLOW)⚠️  This will delete all CSV data files. Are you sure? [y/N]$(NC)" && read ans && [ $${ans:-N} = y ]
	@rm -f databag/performance-monitoring.csv databag/performance-snapshot.csv
	@echo "$(GREEN)✅ CSV data files cleared$(NC)"

##@ Maintenance Commands

.PHONY: clean
clean: ## 🧹 Clean cache files and temporary files
	@echo "$(BLUE)🧹 Cleaning cache and temporary files...$(NC)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache build dist
	@echo "$(GREEN)✅ Cache files cleaned!$(NC)"

.PHONY: clean-logs
clean-logs: ## 📝 Clean log files
	@echo "$(BLUE)📝 Cleaning log files...$(NC)"
	@rm -rf app/logs/*.log
	@echo "$(GREEN)✅ Log files cleaned!$(NC)"

.PHONY: clean-all
clean-all: clean clean-logs ## 🗑️ Complete cleanup (cache, logs, virtual environment)
	@echo "$(BLUE)🗑️ Removing virtual environment...$(NC)"
	@rm -rf $(VENV_DIR)
	@echo "$(GREEN)✅ Complete cleanup finished!$(NC)"

.PHONY: reset
reset: clean-all setup ## 🔄 Complete reset (clean everything and setup fresh)
	@echo "$(GREEN)🔄 Project reset complete!$(NC)"

##@ Information Commands

.PHONY: status
status: ## 📋 Show project status and information
	@echo "$(BLUE)📋 Task Monitor Project Status$(NC)"
	@echo "================================="
	@echo ""
	@echo "$(YELLOW)Virtual Environment:$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "  ✅ Virtual environment exists"; \
		echo "  📍 Location: $(VENV_DIR)"; \
		echo "  🐍 Python: $$($(PYTHON_VENV) --version 2>/dev/null || echo 'Not accessible')"; \
	else \
		echo "  ❌ Virtual environment not found"; \
	fi
	@echo ""
	@echo "$(YELLOW)Data Files:$(NC)"
	@if [ -f "databag/performance-monitoring.csv" ]; then \
		echo "  ✅ performance-monitoring.csv ($$(wc -l < databag/performance-monitoring.csv) lines)"; \
	else \
		echo "  ❌ performance-monitoring.csv not found"; \
	fi
	@if [ -f "databag/performance-snapshot.csv" ]; then \
		echo "  ✅ performance-snapshot.csv ($$(wc -l < databag/performance-snapshot.csv) lines)"; \
	else \
		echo "  ❌ performance-snapshot.csv not found"; \
	fi
	@echo ""
	@echo "$(YELLOW)Directories:$(NC)"
	@ls -la | grep ^d || echo "  No directories found"

.PHONY: urls
urls: ## 🌐 Show application URLs
	@echo "$(BLUE)🌐 Application URLs:$(NC)"
	@echo "  Dashboard: http://localhost:$(PORT)"
	@echo "  Test Charts: http://localhost:$(PORT)/test-charts"

##@ Help

.PHONY: help
help: ## 💡 Show this help message
	@echo "$(BLUE)Task Monitor Application - Available Commands$(NC)"
	@echo "=============================================="
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-18s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(YELLOW)%s$(NC)\n", substr($$0, 5) }' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BLUE)Quick Start:$(NC)"
	@echo "  1. make setup     # Set up the project"
	@echo "  2. make run       # Start the dashboard"
	@echo "  3. make monitor   # Start continuous monitoring"
	@echo ""
	@echo "$(BLUE)Examples:$(NC)"
	@echo "  make monitor-limited LIMIT=15  # Monitor top 15 processes"
	@echo "  make dev                       # Run in development mode"
	@echo "  make clean && make setup       # Fresh reinstall"