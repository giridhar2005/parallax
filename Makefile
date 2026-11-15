.PHONY: help setup dev desktop fixture test lint format frontend-build icon app dmg clean

help:
	@echo "Parallax Developer & Release Commands:"
	@echo "  make setup          Install backend & frontend dependencies"
	@echo "  make dev            Run FastAPI backend server in reload mode"
	@echo "  make desktop        Launch native macOS desktop application"
	@echo "  make fixture        Seed SQLite database with forensic deposition case data"
	@echo "  make test           Run full pytest suite (18 tests)"
	@echo "  make lint           Check Python code quality with Ruff"
	@echo "  make format         Auto-format codebase with Ruff"
	@echo "  make frontend-build Build React TypeScript workbench (frontend/dist)"
	@echo "  make icon           Generate high-res Parallax.icns icon bundle"
	@echo "  make app            Compile standalone macOS Parallax.app bundle"
	@echo "  make dmg            Build complete macOS drag-to-Applications .dmg installer"
	@echo "  make clean          Clean build caches, temporary SQLite WAL files, and artifacts"

setup:
	uv pip install -e ".[dev]"
	cd frontend && npm install

dev:
	uv run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

desktop:
	uv run python -m backend.desktop

fixture:
	uv run python -c "from backend.app.services.fixtures import seed_fixtures; print(seed_fixtures())"

test:
	uv run pytest -v

lint:
	uv run ruff check backend tests

format:
	uv run ruff format backend tests

frontend-build:
	cd frontend && npm run build

icon:
	uv run python packaging/make_icon.py

app: frontend-build icon
	uv run pyinstaller --clean -y packaging/Parallax.spec

dmg:
	./packaging/build_dmg.sh

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__ */__pycache__ */*/__pycache__
	rm -rf dist build release frontend/dist
	rm -f data/parallax.db-shm data/parallax.db-wal packaging/Parallax.iconset
