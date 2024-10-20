setup:
	pip install -r requirements.txt
	python -m playwright install --with-deps chromium

run:
	python main.py

build:
	docker build -t curtpark/monolithic_server:latest .

push:
	docker push curtpark/monolithic_server:latest

run-docker:
	docker run -it --rm -p 9888:9888 curtpark/monolithic_server:latest
