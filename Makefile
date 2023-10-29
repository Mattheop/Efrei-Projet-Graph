deploy:
	ansible-playbook -i hosts playbook.yml

local:
	docker compose up -d --build --force-recreate -V

down:
	docker compose down

dev:
	docker compose -f docker-compose.dev.yml up --force-recreate -V --build

