install_dependencies:
	pip install -r requirements.txt

local_test:
	export DB_CONNECTION_STATUS=$$? && \
	uv run -m uvicorn src.app.main:app --port 8000 --log-level debug --reload

alembic_revision:
	@echo "Please enter a message for the review:"
	@read MESSAGE; \
	rev_id=$$(date -u +"%Y%m%d%H%M%S"); \
	uv runalembic -c ./src/alembic.ini revision -m "$$MESSAGE" --rev-id="$$rev_id"

alembic_autogenerate_revision:
	@echo "Please enter a message for the review:"
	@read MESSAGE; \
	rev_id=$$(date -u +"%Y%m%d%H%M%S"); \
	uv run alembic -c ./src/alembic.ini revision --autogenerate -m "$$MESSAGE" --rev-id="$$rev_id"

alembic_upgrade:
	uv run alembic -c ./src/alembic.ini upgrade head

alembic_downgrade:
	uv run alembic -c ./src/alembic.ini downgrade base

alembic_history:
	uv run alembic -c ./src/alembic.ini history

reset_db:
	uv run alembic -c ./src/alembic.ini downgrade base && uv run alembic -c ./src/alembic.ini upgrade head && uv run alembic -c ./src/alembic.seeders.ini -x env=seeders upgrade head

docker_compose_up:
	docker compose --env-file .env.docker up
