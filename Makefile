
ifneq ($(shell which docker-compose 2>/dev/null),)
    DOCKER_COMPOSE := docker-compose
else
    DOCKER_COMPOSE := docker compose
endif

install:
	$(DOCKER_COMPOSE) up -d

remove:
	@$(DOCKER_COMPOSE) down

start:
	$(DOCKER_COMPOSE) start

startAndBuild: 
	$(DOCKER_COMPOSE) up -d --build

stop:
	$(DOCKER_COMPOSE) stop

pyrequire:
	@pip install -r dev-requirements.txt
py:
	@python -m build --no-isolation --outdir dist/

pyclean:
	rm -rf dist/

update:
	@git pull
	$(DOCKER_COMPOSE) down
	@docker stop tread || true
	$(DOCKER_COMPOSE) up --build -d
	$(DOCKER_COMPOSE) start
