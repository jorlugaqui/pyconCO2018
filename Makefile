PROJECT_NAME=pycon

build: 
	sudo docker build -t jorlugaqui/pycon:latest .

test:
	sudo docker-compose -f docker-compose.ci.yml run api-test python3.6 manage.py test --verbosity=2

rm-tmp-env: 
	rm .env.tmp

rm-env:
	rm .env

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
	sudo docker-compose up

down:
	sudo docker-compose down 

ci-down:
	sudo docker-compose -f docker-compose.ci.yml down

status:
	sudo docker ps -a

replace-env: rm-env subst rm-tmp-env

copy-env: env-tmp replace-env

copy-env-ci: env-tmp-ci replace-env

dev: copy-env build rm-override copy-compose-override run

ci: copy-env-ci replace-env build rm-override test ci-down

