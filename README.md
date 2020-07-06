# Rate Limiting Service
A random number generator with limiting access with only 5 requests in a miniute.
Here Django-ratelimit is used for limiting.

## Installation

setup virtualenvironment and clone repository

```bash
sudo apt-get install python3-venv
python3 -m venv ./venv
source ./venv/bin/activate
git clone https://github.com/suryamunirathinam/RandomNumber.git
cd RandomNumber
````

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies

```bash
pip install -r requirements.txt
```

## Usage

```python
python manage.py migrate
python manage.py runserver
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
