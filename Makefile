
zip:
	pip install --upgrade pip
	cd server && pip3 install --target ./lib/ --requirement requirements.txt
	rm -rf ./server/lib/*dist-info
	cd server && zip -r lambda.zip ./*.py
	touch ./server/lib/__init__.py
	cd server/lib && zip -r9 ../lambda.zip ./*
	mv ./server/lambda.zip ./cdk/lambda.zip

synth:
	cd cdk && cdk synth

diff:
	cd cdk && cdk diff

deploy:
	cd cdk && cdk deploy
