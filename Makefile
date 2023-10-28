run:
	docker run --gpus all --env-file .env -it -p 5000:5000 flask-app

# run container in background
run-bg:
	docker run --gpus all --env-file .env -it -p 5000:5000 -d flask-app

build:
	docker build -t flask-app .