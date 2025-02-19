docker_setup:
	docker volume create pgadmin-local
	docker volume create postgres-local
	docker volume create postgres-llm
	docker volume create postgres-external
