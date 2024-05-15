# Local setup environment

Run "pip-compile --output-file=requirements/prod.txt pyproject.toml" to create package dependencies for the project
Run "pip-compile --extra test -o requirements/test.txt pyproject.toml" to create package dependencies for the testing
Run "pip-compile --extra dev -o requirements/dev.txt pyproject.toml" to create package dependencies for the development

# Install requirements files

Run "pip install -r requirements/prod.txt ."
When developing run "pip install -r requirements/dev.txt ."
When testing run "pip install -r requirements/test.txt --editable ."
