### Setting up the project
1. Clone the project on local machine
2. Create a virtual environment
```python -m venv venv/```
3. Activate the virtual environment
```source venv/bin/activate```
4. Install project dependencies
```pip install -r requirements.txt```
5. Run the DB migrations
```python manage.py migrate```
6. Run the script to read the orders from the XML feed
```python manage.py import_orders```
7. Run the Django server
```python manage.py runserver```
8. Check the 2 endpoints at:
```http://127.0.0.1:8000/orders``` and ```http://127.0.0.1:8000/orders/111-2222222-3333333```
