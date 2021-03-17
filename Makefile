IMAGE_NAME = weather_app_flask
VERSION = 1.0

build:
	docker build -t $(IMAGE_NAME):$(VERSION) .
run:
	docker run -p 1400:5000 --name image --rm $(IMAGE_NAME):$(VERSION)
lint:
	docker run --rm -v $(PWD):/code eeacms/pylint