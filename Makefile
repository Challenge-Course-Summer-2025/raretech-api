up:
	docker compose up --build

up-d:
	docker compose up -d

ps:
	docker compose ps

logs:
	docker compose logs

exec-app:
	docker compose exec web bash

exec-dynamodb:
	docker compose exec dynamodb bash

down:
	docker compose down