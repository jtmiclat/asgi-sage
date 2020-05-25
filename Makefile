SOURCE_FILES = asgi_sage tests
install:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
	poetry install -v

lint:
	poetry run black --target-version=py36 ${SOURCE_FILES}
	poetry run isort --recursive --apply ${SOURCE_FILES}
	poetry run flake8 ${SOURCE_FILES}
	poetry run mypy asgi_sage

test:
	poetry run python -m pytest

coverage:
	poetry run coverage report --show-missing --skip-covered --fail-under=97