
local_setup_linux:
	sudo snap install terraform --classic


zip:
	pip install --upgrade pip
	cd server && pip3 install --target ./lib/ --requirement requirements.txt
	rm -rf ./server/lib/*dist-info
	cd server && zip -r lambda.zip ./*.py
	touch ./server/lib/__init__.py
	cd server/lib && zip -r9 ../lambda.zip ./*
	mv ./server/lambda.zip ./cdk/job_board/api/lambda.zip
	chmod 755 ./cdk/job_board/api/lambda.zip

plan:
	cd cdk && cdktf plan

apply:
	cd cdk && cdktf apply