# mongo-py-logger
Python logger based on logging with mongoDB handle.

Example:
```python
from mongo_py_logger.logger import *
logger = MongoLogger(
'MONGODB_CONNECTION_STRING', cert_pth='path/to/client.pem',
    collection_name='name_of_my_collection',
    name='my_logger',
    additional_field = "my_additional_data")
```