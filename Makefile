install:
	python -m venv venv
	./venv/Scripts/activate && pip install -r requirements.txt

lint:
	flake8 src
	black --check src
	mypy src

test:
	pytest tests --cov=src

data:
	python src/data/commodity_loader.py
	python src/data/materials_project.py
	python src/data/nbi_loader.py

features:
	python src/features/build_features.py

train:
	python src/models/train_model.py

dashboard:
	streamlit run src/dashboard/app.py

docker:
	docker-compose up --build

docs:
	cd docs && sphinx-build -b html . _build/html

all: install data features train dashboard
