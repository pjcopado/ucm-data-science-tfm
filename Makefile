docker_create_volumes:
	docker volume create postgres_data
	docker volume create postgres-external
	docker volume create postgres-local
	docker volume create pgadmin-local
