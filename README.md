# vendomatic

## Steps to Install this App

1. Clone this repo onto your computer
- ` git clone git@github.com:melliemuse/vendomatic-rest.git `

2. Create Virtual Environment
- ` cd vendomatic-rest `
- ` python -m venv VendomaticEnv `

3. Activate Virtual Environment
- ` source ./OfAFeatherEnv/bin/activate `

4. Install Dependencies
- ` pip install -r requirements.txt `

5. Build Database from Models 
- ` python manage.py makemigrations vendomatic `
- ` python manage.py migrate `

6. Create a Superuser 
- ` python manage.py createsuperuser `

7. Load data from fixtures into your database
- ` python manage.py loaddata fixtures/fixtures.json`

8. Run Server 
- ` python manage.py runserver `

How to Use this App

HTTP requests can be tested using Postman

Coins: 

To test for adding a coin:
PUT to the '/' endpoint can be tested by running a PUT at 'http://localhost:8000/'
After running DELETE and clearing out Coin entries, you will have to manually add a coin to the database using TablePlus for a PUT to work

To test for returning change:
Delete to the '/' endpoint can be tested by running a DELETE at 'http://localhost:8000/$[id]'


Inventory:

To See A List Reflecting Current Inventory:
Run a GET at 'http://localhost:8000/inventory'

To See Current Stock by Inventory Item:
Run a GET at 'http://localhost:8000/inventory/$[id]'

To Vend a Beverage:
Run a PUT at 'http://localhost:8000/inventory/$[id]' (where id == beverage.id)
