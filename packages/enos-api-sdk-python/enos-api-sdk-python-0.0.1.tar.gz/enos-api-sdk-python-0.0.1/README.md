# Using EnOS Service SDK for Python (Preview Edition)

This repo contains the preview edition of EnOS Service SDK for Python. This article instructs how to prepare your development environment and use the EnOS Service SDK for Python.

* [Installing Python](#python)
* [Obtaining EnOS API SDK for Python](#obtaining)
* [Key Features](#keyfeatures)
* [API Reference](#apiref)
* [Sample Code](#samplecode)

<a name="python"></a>
## Installing Python
To use the EnOS Service SDK for Python, you will need Python 2.7.10+, and `pip` is required.

<a name="obtaining"></a>
## Obtaining EnOS API SDK for Python
You can obtain the SDK through the following methods:

- Install from pip
- Download the source code by cloning this repo and build on your machine

### Install from PIP
```bash
pip install enos-api-sdk-python
```

### Build from source code
1. Obtain the EnOS API SDK for Python source code from GitHub:
    ```
    git clone https://github.com/EnvisionIot/enos-api-sdk-python.git
    ```

2. From the directory where the source code is stored, run the following command:
```bash
python setup.py install
```

<a name="keyfeatures"></a>
## Key Features

As the preview edition, the EnOS Service SDK currently contains only partial of the EnOS Service REST API features as listed below:

- Apply certificate by device key
- Post measure point data
- List and create products

<a name="apiref"></a>
## API Reference
To access the EnOS API documentation, go to **EnOS API > API Documents** in the EnOS Console. For each service category, you can check the summary of the APIs from the API list table and click the **More** icon for view details of each specific API, including API description, calling method, requesting URL, parameter description, calling sample, and response sample.

<a name="samplecode"></a>
## Sample Code

This sample demonstrates how to post a struct type of measure point to the EnOS cloud.

```python
from enosapi.request.PostMeasurepointsEnOSRequest import PostMeasurepointsEnOSRequest
from enosapi.client.EnOSDefaultClient import EnOSDefaultClient
import time
import json

enos_api_url = "https://{HOST}/enosapi/"

# the application configuration created in console
access_key = "ACCESS_KEY"
secret_key = "SECRET_KEY"

# sub-device parameters
device_asset_id = 'DEVICE_ASSET_ID'
product_key = 'PRODUCT_KEY'

# OU ID
org_id = "OU_ID"


if __name__ == "__main__":
    timestamp = int(time.time() * 1000)        # timestamp in milliseconds
    struct_measure_point = {'RawImage': 'local://file1',
             'ProcessedImage': 'local://file2',
             'Sensor': 'PM10',
             'UpperLimit': 100,
             'Value': 120,
             'AlertFlag': 1,
             'AlertMessage': 'PM10 over limit'}

    measure_points = {
        'StructMeasurePoint1': struct_measure_point  # the StructMeasurePoint1 is the identity of a measure point
    }

    data = [{
        'measurepoints': measure_points,
        'assetId': device_asset_id,
        'time': timestamp
    }]

    param = {
        "data": json.dumps(data)
    }

    file_to_upload = {"file1": open("apple.png", 'rb'), "file2": open("orange.png", 'rb')}

    request = PostMeasurepointsEnOSRequest(org_id=org_id, product_key=product_key,
                                           params=param, upload_file=file_to_upload)

    enos_api_client = EnOSDefaultClient(enos_api_url, access_key, secret_key)

    response = enos_api_client.execute(request)
    print(response)
```
