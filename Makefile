PROJECT_NAME=pycon

build: 
	docker build -t jorlugaqui/pycon:latest .

test:
	docker-compose -f docker-compose.ci.yml run api-test python3.6 manage.py test --verbosity=2

rm-tmp-env: 
	rm -f .env.tmp

rm-env:
	rm -f .env

rm-override:
	rm -f docker-compose.override.yml

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

down:
	docker-compose down 

ci-down:
	docker-compose -f docker-compose.ci.yml down

status:
	docker ps -a

replace-env: rm-env subst rm-tmp-env

copy-env: env-tmp replace-env

copy-env-ci: env-tmp-ci replace-env

dev: copy-env build rm-override copy-compose-override run

ci: copy-env-ci replace-env build rm-override test ci-down
