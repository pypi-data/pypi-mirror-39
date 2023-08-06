# python-sdk

- [Installation](#installation)
- [Requirements](#internal-api-implementation)
- [Internal API implementation](#requirements)
- [Quick start and examples](#quick-start-and-examples)
- [Error handling](#error-handling)
- [Advanced usage](#advanced-usage)

---

### Installation

This Python2 version of the SDK can be installed through pip.

Pip is the package manager for Python.

For more information on how to use/install pip, please visit: [https://pypi.org/project/pip/](https://pypi.org/project/pip/)

To install the Pay.nl Python2 sdk into your project, simply

	$ pip install paynlsdk2

### Requirements

The Pay.nl Python SDK works on Python 2 and is dependent on the requests package and the marshmallow package (v2.x only)
When installing through pip these dependencies will automatically be detected and installed

### Internal API implementation
Not all function arguments will be completely described for every case.
When using the utility/quick start classes all parameters are available, so take a look at the method arguments there for more options.
They are basically self explanatory

Every API implementation has it's own Request and Response class, which can be found in the various *paynlsdk2.api.xxx.yyy* modules.
Every one of the modules contain at least a Request and a Response class.
For example, the Transaction.info API can be located in the *paynlsdk2.api.transation.info* module and will contain both a
*paynlsdk2.api.transaction.info.Request* and a *paynlsdk2.api.transaction.info.Response* class 
Usually these modules will also contain a specific (marshmallow) Schema implementation that defines the response mapping from JSON. 

For every call, a response object will be returned.
Using the *print(result)* statement, or by investigating the *paynlsdk2.objects* module, you can find out what attributes are available.
Every result will contain a *request* object, which essentially gives insight on the success or failure of the request.
This object is also used to throw a *paynlsk.exceptions.ErrorException* in case the request failed.
The rest of the *response* object will contain the information as returned by the PAYL API

Again, refer to the *paynlsdk2.objects* module to investigate the various objects contained in the response.
The exact contents of the response objects itself are defined in all the *paynlsdk2.api.xxx.yyy.Response* classes



### Quick start and examples
Do note this quick start only makes use of the quick-call utility methods.
If you're more familiar with Python, you *could* use the full API request/response implementations in the paynlsdk2.api namespace

Set configuration (this is a MUST and should always be done before doing anything with the SDK)
```
from paynlsdk2.api.client import APIAuthentication
APIAuthentication.service_id = 'SL-xxxx-xxxx'
APIAuthentication.api_token = '<yourtokenhere>'
APIAuthentication.token_code = 'AT-xxxx-xxxx'
```

Turn on debugging output for the API Client
Note: this uses "print" and will cause a dump of relevant information to the console such as the endpoint, 
HTTP method, request parameters, http headers and the raw response as a result from the API call
```
from paynlsdk2.api.client import APIClient
APIClient.print_debug = True
```

Get banks (ideal banks only)
```python
# Import needed modules
from paynlsdk2.api.client import APIAuthentication
from paynlsdk2.client.transaction import Transaction
from paynlsdk2.exceptions import *
# Set mandatory basics
APIAuthentication.service_id = 'SL-xxxx-xxxx'
APIAuthentication.api_token = '<yourtokenhere>'
APIAuthentication.token_code = 'AT-xxxx-xxxx'
# Perform request
try:
    result = Transaction.get_banks()
    for bank in result:
        print('{id}: {name}'.format(id=bank.id, name=bank.name))
except SchemaException as se:
    print('SCHEMA ERROR:\n\t' + str(se))
    print('\nSCHEMA ERRORS:\n\t' + str(se.errors))
except ErrorException as ee:
    print('API ERROR:\n' + str(ee))
except Exception as e:
    print('GENERIC EXCEPTION:\n' + str(e))
```

Get list of payment methods
```python
# Import needed modules
from paynlsdk2.api.client import APIAuthentication
from paynlsdk2.client.paymentmethods import PaymentMethods
from paynlsdk2.exceptions import *
# Set mandatory basics
APIAuthentication.service_id = 'SL-xxxx-xxxx'
APIAuthentication.api_token = '<yourtokenhere>'
APIAuthentication.token_code = 'AT-xxxx-xxxx'
# Perform request
try:
    result = PaymentMethods.get_list()
    for payment_method in result.values():
        print('{id}: {name} ({visible_name})'.format(id=payment_method.id, name=payment_method.name,
                                                     visible_name=payment_method.visible_name))
except SchemaException as se:
    print('SCHEMA ERROR:\n\t' + str(se))
    print('\nSCHEMA ERRORS:\n\t' + str(se.errors))
except ErrorException as ee:
    print('API ERROR:\n' + str(ee))
except Exception as e:
    print('GENERIC EXCEPTION:\n' + str(e))
```

Retrieving transaction info
```python
# Import needed modules
from paynlsdk2.api.client import APIAuthentication
from paynlsdk2.client.transaction import Transaction
from paynlsdk2.exceptions import *
# Set mandatory basics
APIAuthentication.service_id = 'SL-xxxx-xxxx'
APIAuthentication.api_token = '<yourtokenhere>'
APIAuthentication.token_code = 'AT-xxxx-xxxx'
# Perform request
try:
    result = Transaction.info(transaction_id='1234567890X1a2b3')
    print(result)
except SchemaException as se:
    print('SCHEMA ERROR:\n\t' + str(se))
    print('\nSCHEMA ERRORS:\n\t' + str(se.errors))
except ErrorException as ee:
    print('API ERROR:\n' + str(ee))
except Exception as e:
    print('GENERIC EXCEPTION:\n' + str(e))
```

Retrieving transaction status 
```python
# Import needed modules
from paynlsdk2.api.client import APIAuthentication
from paynlsdk2.client.transaction import Transaction
from paynlsdk2.exceptions import *
# Set mandatory basics
APIAuthentication.service_id = 'SL-xxxx-xxxx'
APIAuthentication.api_token = '<yourtokenhere>'
APIAuthentication.token_code = 'AT-xxxx-xxxx'
# Perform request
try:
    result = Transaction.status(transaction_id='1234567890X1a2b3')
    print(result)
except SchemaException as se:
    print('SCHEMA ERROR:\n\t' + str(se))
    print('\nSCHEMA ERRORS:\n\t' + str(se.errors))
except ErrorException as ee:
    print('API ERROR:\n' + str(ee))
except Exception as e:
    print('GENERIC EXCEPTION:\n' + str(e))
```


Refunding (part of) a transaction
```python
# Import needed modules
from paynlsdk2.api.client import APIAuthentication
from paynlsdk2.client.transaction import Transaction
from paynlsdk2.exceptions import *
# Set mandatory basics
APIAuthentication.service_id = 'SL-xxxx-xxxx'
APIAuthentication.api_token = '<yourtokenhere>'
APIAuthentication.token_code = 'AT-xxxx-xxxx'
# Perform request
try:
    result = Transaction.refund(transaction_id='1234567890X1a2b3')
    # Whenever you want to partially refund use e.g. (note: amounts are in cents)
    # result = Refund.transaction(transaction_id='1234567890X1a2b3', amount=500, description='partial refund')
    # PLEASE NOTE the refund_id is NOT guaranteed, it will only be returned when the refund is done through IBAN.
    # This is a known flaw, so please do not rely on the refund ID to be part of the response by default
    print('Refund ID: {refund_id}'.format(refund_id=result.refund_id))
except SchemaException as se:
    print('SCHEMA ERROR:\n\t' + str(se))
    print('\nSCHEMA ERRORS:\n\t' + str(se.errors))
except ErrorException as ee:
    print('API ERROR:\n' + str(ee))
except Exception as e:
    print('GENERIC EXCEPTION:\n' + str(e))
```

Refunding (part of) a transaction (alternative method: more request options are available in this API).
```python
# Import needed modules
from paynlsdk2.api.client import APIAuthentication
from paynlsdk2.client.refund import Refund
from paynlsdk2.exceptions import *
# Set mandatory basics
APIAuthentication.service_id = 'SL-xxxx-xxxx'
APIAuthentication.api_token = '<yourtokenhere>'
APIAuthentication.token_code = 'AT-xxxx-xxxx'
# Perform request
try:
    result = Refund.transaction(transaction_id='1234567890X1a2b3')
    # Whenever you want to partially refund use e.g. (note: amounts are in cents)
    # result = Refund.transaction(transaction_id='1234567890X1a2b3', amount=500, description='partial refund')
    # PLEASE NOTE the refund_id is NOT guaranteed, it will only be returned when the refund is done through IBAN.
    # This is a known flaw, so please do not rely on the refund ID to be part of the response by default
    print('Refund ID: {refund_id}'.format(refund_id=result.refund_id))
except SchemaException as se:
    print('SCHEMA ERROR:\n\t' + str(se))
    print('\nSCHEMA ERRORS:\n\t' + str(se.errors))
except ErrorException as ee:
    print('API ERROR:\n' + str(ee))
except Exception as e:
    print('GENERIC EXCEPTION:\n' + str(e))
```

Retrieving refund info
Note: refund ids come in the form of 'RF-xxxx-xxxx'
```python
# Import needed modules
from paynlsdk2.api.client import APIAuthentication
from paynlsdk2.client.refund import Refund
from paynlsdk2.exceptions import *
# Set mandatory basics
APIAuthentication.service_id = 'SL-xxxx-xxxx'
APIAuthentication.api_token = '<yourtokenhere>'
APIAuthentication.token_code = 'AT-xxxx-xxxx'
# Perform request
try:
    result = Refund.info(refund_id='RF-1234-1234')
    print(result)
except SchemaException as se:
    print('SCHEMA ERROR:\n\t' + str(se))
    print('\nSCHEMA ERRORS:\n\t' + str(se.errors))
except ErrorException as ee:
    print('API ERROR:\n' + str(ee))
except Exception as e:
    print('GENERIC EXCEPTION:\n' + str(e))
```

Starting a transaction
```python
# Import needed modules
from paynlsdk2.api.client import APIAuthentication
from paynlsdk2.client.transaction import Transaction
from paynlsdk2.objects import OrderData, Address, Company, datetime, TransactionEndUser,\
    TransactionStartStatsData, TransactionData, SalesData
from paynlsdk2.exceptions import *
# Set mandatory basics
APIAuthentication.service_id = 'SL-xxxx-xxxx'
APIAuthentication.api_token = '<yourtokenhere>'
APIAuthentication.token_code = 'AT-xxxx-xxxx'
# Perform request
try:
    saledata = SalesData()
    saledata.invoice_date = datetime(2018,10,30)
    saledata.delivery_date = datetime(2018,11,1)
    order_data = OrderData(product_id='XYZ', product_type='ARTICLE', description='XYZ description',
                           price=900, quantity=1, vat_code='H', vat_percentage=21)
    saledata.order_data.append(order_data)
    
    enduser = TransactionEndUser(language='nl', initials='A', last_name='Jansen', gender='m', dob=datetime(1970,1,2),
                                 phone_number='0612345678', email_address='someone@somewhere.com', iban='<ibannumber>',
                                address=Address(initials='A', last_name='Jansen', gender='m', 
                                                street_name='Street', street_number='1', street_number_extension='A', 
                                                zip_code='1234AB', city='Rotterdam', region_code='ZH', 
                                                country_code='NL', country_name='Nederland'),
                                invoice_address=Address(initials='A', last_name='Jansen', gender='m', 
                                                        street_name='Street', street_number='1', street_number_extension='A', 
                                                        zip_code='1234AB', city='Rotterdam', region_code='ZH', 
                                                        country_code='NL', country_name='Nederland'),
                                 company=Company(name='Wizard Inc', coc_number='12345678',
                                                vat_number='NL123456789B01', country_code='NL')
                                 )
    
    sinfo1 = {'amount': 250, 'ip_address': '192.168.0.1', 'finish_url': 'https://somedomain.com', 'payment_option_id': 436,
              'transaction': TransactionData(description='order 9999 at Wizard Inc', order_number='9999', 
                                             order_exchange_url='https://somedomain.nl/exchange.php'),
              'stats_data': TransactionStartStatsData(extra1='IDX 9999'),
              'end_user': enduser,
              'sale_data': saledata,
              'test_mode': True
              }
    
    result = Transaction.start(**sinfo1)
    # print(result)
    print('Transaction ID: {id}\nPayment reference: {ref}\nPayment URL: {url}'.format(
            id=result.transaction.transaction_id, ref=result.get_payment_reference(), url=result.get_redirect_url()))
except SchemaException as se:
    print('SCHEMA ERROR:\n\t' + str(se))
    print('\nSCHEMA ERRORS:\n\t' + str(se.errors))
except ErrorException as ee:
    print('API ERROR:\n' + str(ee))
except Exception as e:
    print('GENERIC EXCEPTION:\n' + str(e))
    
```

### Error handling
You should always wrap your calls in an exception handler.
The SDK only contains four internal exceptions:
- paynlsdk2.exceptions.ErrorException

  If, for any reason, an error arises in the communication or internally in the API, this exception will be thrown
- paynlsdk2.exceptions.SchemaException

  If, for any reason, the schema mapping (using marshmallow), shall fail , this exception is thrown

- paynlsdk2.exceptions.TransactionNotAuthorizedException

  This exception is only thrown whenever you try to _void_ or _capture_ a transaction using the Response instance as a
  result of a call to Transaction.info()

- paynlsdk2.exceptions.TransactionStatusException

  This exception is only thrown whenever you try to _approve_ or _decline_ a transaction using the Response instance as a
  result of a call to Transaction.info()

Note: it can always happen that any other standard exceptions are thrown.
These are most likely to happen outside of the SDK but should also be handled.

### Advanced usage
Whenever you want to make use of the Request and Response objects yourself for any purpose, you always have the option
of creating the request object for any API call. These can be found in any of the paynlsdk2.api.xxx.yyy modules.
This gives you the advantage of being able to get to the raw requests parameters as well as the raw responses as 
returned by Pay.nl.
Although you shouldn't normally need to, below is a complete example of this
```python
import json
from paynlsdk2.api.transaction.info import Request
from paynlsdk2.api.client import APIAuthentication, APIClient

APIAuthentication.service_id = 'SL-xxxx-xxxx'
APIAuthentication.api_token = '<yourtokenhere>'
APIAuthentication.token_code = 'AT-xxxx-xxxx'

# Create request.
request = Request(transaction_id='1234567890X1a2b3')
# Send request.
response = APIClient.perform_request(request)
# We now basically have all information
# Display raw request parameters:
parameters = request.get_parameters()
print('Request parameters:\n')
print(format(json.dumps(parameters)))
# Display raw response:
print('Raw response:\n')
print(request.raw_response)
print('Response class: ' + type(request.response))
```
