
zip:
	pip install --upgrade pip
	cd server && pip3 install --target ./lib/ --requirement requirements.txt
	rm -rf ./server/lib/*dist-info
	touch ./server/lib/__init__.py
	cd server && zip ./lambda.zip ./*.py ./db/*.py ./views/*.py
	cd server/lib && zip -r9 ../lambda.zip ./*
	mv ./server/lambda.zip ./cdk/lambda.zip

synth:
	cd cdk && cdk synth

diff:
	cd cdk && cdk diff

deploy:
	cd cdk && cdk deploy

run:
	cd server && python3 ./main.py

start:
	cd client && HTTPS=true npm start

CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)
VERSION=$(shell date '+%Y-%m-%d')
update_client:
	rm -rf ./client
	curl http://localhost:5000/openapi.json -o openapi.json
	docker run --rm \
		--user "${CURRENT_UID}:${CURRENT_GID}" \
		-v $(PWD):/local \
		openapitools/openapi-generator-cli:latest \
		generate \
		-i /local/openapi.json \
		-g javascript-axios \
		--additional-properties=supportsES6=true  \
		-o /local/client/src/api_client
	rm openapi.json
