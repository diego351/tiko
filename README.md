![alt text](https://github.com/diego351/tiko/blob/master/image.png?raw=true)

# Usage

1. Assuming you have latest python3 installed, checkout repo
2. `cd tiko/tiko_assignment`
3. `python3 -m venv .venv`
4. `source .venv/bin/activate`
5. `pip install -r requirements.txt`
6. `python manage.py migrate`
7. `python manage.py runserver`
8. Open in browser `localhost:8000/api/docs`
9. Register new user with `register_create` endpoint, remember `access` token value
10. Login using `token_create` pasting plain token to Token field, pass email as username
11. Play with entire api as you wish

# TODO:

1. tests
2. email verification
3. interactive api tuning
