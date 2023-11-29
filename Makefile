.PHONY: all

install:
	.venv/bin/pip3 install -r requirements.txt

dev:
	.venv/bin/uvicorn server.main:app --reload

run:
	.venv/bin/uvicorn server.main:app
