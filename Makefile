
zip_server:
	pip install --upgrade pip
	cd server && pip3 install --target ./lib/ --requirement requirements.txt
	rm -rf ./server/lib/*dist-info
	touch ./server/lib/__init__.py
	cd server && zip ./lambda.zip ./*.py ./db/*.py ./views/*.py
	cd server/lib && zip -r9 ../lambda.zip ./*
	mv ./server/lambda.zip ./cdk/lambda.zip

synth_infra:
	cd cdk && cdk synth

diff_infra:
	cd cdk && cdk diff

deploy_infra:
	cd cdk && cdk deploy --all

deploy_server: zip_server deploy_infra

deploy_client:
	cd client && npm run build
	cd client && aws s3 sync ./build/ s3://yyjtechjobboard.ca
	cd client && aws cloudfront create-invalidation --distribution-id=EP3UB04VUQG2S --paths=/index.html


run_local_server:
	cd server && python3 ./main.py

start_local_client:
	cd client && HTTPS=true npm start

CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)
VERSION=$(shell date '+%Y-%m-%d')
update_client:
	rm -rf ./client/api_client
	curl http://localhost:5000/openapi.json -o openapi.json
	docker run --rm \
		--user "${CURRENT_UID}:${CURRENT_GID}" \
		-v $(PWD):/local \
		openapitools/openapi-generator-cli:latest \
		generate \
		-i /local/openapi.json \
		-g typescript-axios \
		--additional-properties=npmName=job-board-sdk  \
		-o /local/client/api_client
	rm openapi.json
	cd client && npm install ./api_client
