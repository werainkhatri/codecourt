# CodeCourt

Code submission and evaluation plaform using docker for execution and security. It's a court for code, constituting judges of different languages, conducting sessions in their own container.

Currently supports c11, c++14, c++17, c++20, python 2 and python 3, with more to come.

## Getting Started

1. Make sure you have [python](https://www.python.org) and [docker](https://docs.docker.com/get-docker/) installed on your machine.

1. Setup and start virtual environment. If you don't have `python3`, replace with `python`.

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies and migrate

```bash
pip install -r requirements.txt
python manage.py migrate
```

3. Run server and open *localhost:8000* in a browser

```bash
python manage.py runserver
```

4. To test
### This will download the images for specific languages which can be in GBs, so this may run long for the first time. Don't forget to delete the docker instance after this test completes.

```bash
python manage.py test
```
