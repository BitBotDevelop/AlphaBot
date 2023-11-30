.PHONY: all

install:
	.venv/bin/pip3 install -r requirements.txt

dev:
	.venv/bin/uvicorn server.main:app --reload --host 0.0.0.0 --port 8000

run:
	.venv/bin/uvicorn server.main:app --host 0.0.0.0 --port 8000
