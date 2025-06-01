# Django CV Project

## Prerequisites

- Python 3.10 or higher
- pyenv (Python version manager)
- Poetry (Python dependency manager)

## Setup Instructions

### 1. Install pyenv (if not already installed)

#### On macOS:
```bash
python3 -m venv venv
```

### Activate venv
```bash
source venv/bin/activate   
```


### 3. Install Poetry (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 4. Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd DTEAM-django-practical-test
```

2. Install Python 3.10 using pyenv:
```bash
pyenv install 3.10.0
pyenv local 3.10.0
```

3. Install project dependencies using Poetry:
```bash
cd CVProject
pip install poetry 
```

4. Activate the virtual environment:
```bash
poetry shell
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Load initial data from fixtures:
```bash
# Load all fixtures
python manage.py loaddata */fixtures/*.json

# Or load specific fixtures
python manage.py loaddata cv_fixture.json
```

7. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Project Structure

```
CVProject/
├── manage.py
├── CVProject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_views.py
│   │   └── test_models.py
│   ├── templates/
│   │   ├── main/
│   │   │   ├── cv_list.html
│   │   │   └── cv_detail.html
│   │   └── base.html
│   └── fixtures/
│       └── cv_fixture.json
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
├── pyproject.toml
└── poetry.lock
```

## Development

- All dependencies are managed through Poetry
- Use `poetry add <package-name>` to add new dependencies
- Use `poetry update` to update dependencies
- Use `poetry shell` to activate the virtual environment

### Working with Fixtures

Fixtures are JSON files containing initial data for your models. They are stored in the `fixtures` directory of each app.

To load fixtures:
```bash
# Load all fixtures
python manage.py loaddata */fixtures/*.json

# Load specific fixture
python manage.py loaddata cv_fixture.json
```

### Running Tests

The project includes tests for views and models. To run the tests:

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test main.tests.test_views

# Run specific test case
python manage.py test main.tests.test_views.CVListViewTests

# Run with coverage report
coverage run manage.py test
coverage report
coverage html  # Generates HTML report in htmlcov/
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request