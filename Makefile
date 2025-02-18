docker_create_volumes:
	docker volume create pgadmin-local
	docker volume create postgres-local
	docker volume create postgres-llm
	docker volume create postgres-external
