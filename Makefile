PROJECT_NAME=pycon

build: 
	docker build -t jorlugaqui/pycon:latest .

tox:
	docker run --rm --env-file .env jorlugaqui/pycon:latest tox

rm-env: 
	rm .env.tmp

subst:
	envsubst < .env.tmp > .env

env-tmp:
	cp env.local .env.tmp

env-tmp-ci:
	cp env.ci .env.tmp

copy-compose-override:
	cp docker-compose.override.local.yml docker-compose.override.yml

run:
	docker-compose up

replace-env: subst rm-env

copy-env: env-tmp replace-env

copy-env-ci: env-tmp-ci replace-env

dev: copy-env build copy-compose-override run

tests: copy-env-ci build tox

