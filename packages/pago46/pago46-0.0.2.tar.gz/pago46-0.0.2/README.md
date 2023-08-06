# Pago46 Python Package

Python Library for the integration with the cash payment plataform of pago46.

## Description

This library it was developed for give e-merchants of pago46 a standard, easy and fast integration to integrate his products/services with Pago46 to can offer the option of pay with cash to his clients


### Configuration.

to configure the client of Pago46 it's necessary to have a MERCHANT_SECRET and MERCHANT_KEY (those key are provided by Pago46)
with those keys we can generate calls to PAGO46 API.

we must configure the MERCHANT_SECRET, MERCHANT_KEY and PAGO46_API_HOST on enviroment variables.

Example
```python
import os
os.environ["PAGO46_MERCHANT_KEY"] = "<merchant_key>"
os.environ["PAGO46_MERCHANT_SECRET"] = "<merchant_secret>"
os.environ["PAGO46_API_HOST"] = "http://sandboxapi.pago46.com" # for testing  or "https://api.pago46.com" for production
```

with the environment variables set, we can intilialize the client 


```python
from pago46.client import Pago46

client = Pago46()
```
Example Get all orders 
```python
response = client.get_all_orders()
```
Example create a order

```python
from pago46.client import Pago46


client = Pago46()

payload = {
    "currency": "CLP", # Tipo de moneda 
    "merchant_order_id": '0001', # id que identifica una transacción.
    "notify_url":"http://merchant.com/app/response", # La URL en la que pago46 publicara la respuesta al modificarse el estado de la transacción.
    "price": 1000,# precio de la orden
    "return_url": "http://final.merchant.com",# url a la cual el user será redirigido al terminar el proceso.
    "timeout": 60, # duración en que la transacción estará activa para ser pagada en minutos.
    "description": "description of product.", # (opcional): descripción opcional del producto/servicio.

}

# create a new order
response = client.create_order(payload)
```

Example to mark a order as complete.

```python
payload = {"order_id": "0001"}
response = client.mark_order_as_complete(payload)
```
Example get a order by ID

```python
order_id = "0001"
response = client.get_order_by_id(order_id)
```
Example get a order by Notification ID

```python
notification_id = "fe0eac28aa774b539b0e12d0227bf27f"
response=  client.get_order_by_notification_id(notification_id)
```
Example get order details by order ID


```python
order_id = "121d3b2c-b985-4592-b8fc-b5c6d9ce5a13"
response = client.get_order_details_by_order_id(order_id)
```


###  Installation

You can install Pago46 Package in the usual ways. The simplest way is with pip:

```
pip install Pago46
```

