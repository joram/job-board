
local_setup_linux:
	sudo snap install terraform --classic


zip:
	cd server && pip3 install --target ./libs --requirement requirements.txt
	cd server && zip -gq lambda.zip main.py
	mv ./server/lambda.zip ./infra/modules/api-gateway

plan:
	cd infra/env/dev && terraform plan

deploy:
	cd infra/env/dev && terraform apply