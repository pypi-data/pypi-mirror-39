# pynamo

## Introduction

pynamo is a wrapper library for editing dynamo tables.  The current dynamo boto3 library can be challenging to work with:

1) The Dynamo syntax is non-standard and needs to be converted before dictionaries/json are added to the table

2) Some methods (i.e. scan) can only return part of the data due to data limitations

3) Error handling is often unintuitive

With this in mind, the pynamo library was created with some methods added on top to ease communication with dynamo.

## Installation and Setup

pynamo is on pypi.org as a pip package.  As such, it can be install with pip

```bash
sudo pip install pynamo
```

To import the pynamo class, simply include

```python
from pynamo import Pynamo
```

at the top of your python script.

## The Pynamo Class

The Pynamo class is constructed using the same parameters as the [boto3 session class](https://boto3.readthedocs.io/en/latest/reference/core/session.html).  In addtion, an existing boto_session can be used by pointing to it with the boto_session parameter.

### Attributes

The Pynamo has both the boto3 dynamo client and the boto3 session as attributes.  This allows for using the standard boto3 library without creating new clients and sessions.  For instance, if the user needed to call the boto3 method *create_table*, they would simply call

```python
SESSION_INFO = {
    "region_name": 'us-east-1'
}

TABLE_INFO = {
    AttributeDefinitions:[{
        'AttributeName': 'PrimaryKey',
        'AttributeType': 'S'
    }],
    TableName='test_table',
    KeySchema=[{
            'AttributeName': 'PrimaryKey',
            'KeyType': 'HASH'
        }],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
}

Pynamo(**SESSION_INFO).client.create_table(**TABLE_INFO)
```

This works for any standard boto3 dynamo method.

## Methods

If the native boto3 client/session isn't used, the following methods are available with the parameters listed.  In addition to these parameters, any additional parameters will be passed into the corresponding boto3 function.  For example, the boto3 documentation specifies that for the scan method, the attribute 'IndexName' is available.  If this attribute is passed into the scan function, it will also be passed into the inner boto3 scan function.

Furthermore, responses for the functions have been standardized and will not throw errors like their base boto3 counterparts.  They will instead return a dictionary with the following keys:

1) *status:* the status code of the request

2) *data:* the relevent data of the request

3) *error_msg*: the error message if applicable.

It is the responsiblity of the user to the check the status code for errors rather than relying on errors being raised.

### scan(table_name, **kwargs)

scan will scan the entire table, automatically making additional api calls with the previous LastEvaluatedKey in order to get the whole table.  It will then convert the data into a standard dictionary.  Additional arguments that match boto3 syntax can be added in place of **kwargs.

```python
Pynamo(**SESSION_INFO).scan('table-name')
```

### get_item(table_name, key, **kwargs)

get_item will retrieve a specific item corresponding to the key given.  The key should be given as a standard dictionary rather than dynamo syntax.  It will then convert the data into a standard dictionary.  Additional arguments that match boto3 syntax can be added in place of **kwargs.

```python
Pynamo(**SESSION_INFO).get_item('table-name', {
    "AccountNumber": 123456789012
})
```

### put_item(table_name, item, overwrite=False, **kwargs)

put_item will add a given item to the table.  If the overwrite tag is set to true, it will overwrite an existing item if one with a matching key exists.  The item should be given as a standard dictionary rather than dynamo syntax.  It will convert the data into dynamo syntax before adding to the table.  Additional arguments that match boto3 syntax can be added in place of **kwargs.

```python
Pynamo(**SESSION_INFO).put_item('table-name', {
    "AccountNumber": 123456789012,
    "Alias": "poop-prod",
    "Data": ["1 poop", "2 poop", "red poop", "blue poop"]
})
```

### delete_item(table_name, key, **kwargs)

delete_item will delete a specific item corresponding to the key given.  The key should be given as a standard dictionary rather than dynamo syntax.  Additional arguments that match boto3 syntax can be added in place of **kwargs.

```python
Pynamo(**SESSION_INFO).delete_item('table-name', {
    "AccountNumber": 123456789012
})
```

### update_item(table_name, key, attribute_updates, **kwargs)

update_item will update the attributes of an item with a specific key.  The key and attributes should be given as a standard dictionary rather than dynamo syntax.  The attributes should, however, follow standard boto syntax.  It will convert the data into dynamo syntax before adding to the table.  Additional arguments that match boto3 syntax can be added in place of **kwargs.

```python
Pynamo(**SESSION_INFO).update_item('table-name', {"AccountNumber": 123456789012}, {
    "data": {
        "Value": [1, 2, 3],
        "Action": "PUT"
    }
})
```

### replace_item(table_name, original_key, new_item)

replace_item destroys an old item and replaces it with a new one.  The use case is to update an item totally with a new entry rather than with individual attributes.  The original_key and new_item should be given as a standard dictionary rather than dynamo syntax.  If the key value in the new_item is different from the original_key, the entry with the original_key will be deleted to ensure that the update doesn't leave behind old entries.

```python
Pynamo(**SESSION_INFO).replace_item('table-name', {"AccountNumber": 000000000000}, {
    "AccountNumber": 1111111111111,
    "Alias": "poop-prod",
    "Data": ["1 poop", "2 poop", "red poop", "blue poop"]
})
```

### copy_table(source_table, target_table, source_profile=None, target_profile=None, clear_table=False)

copy_table scans a source table and copies the contents to a target table.  If the clear_table flag is set to True, it will delete the target_table first, otherwise it will just append the new entries (overwriting ones with existing key values).  The copy can be performed accross accounts by setting the source_profile and target_profiles to reference different profiles in the aws credentials file, otherwise the session info used for the pynamo object is used for each case.

```python
Pynamo(**SESSION_INFO).copy_table('test-table-pcp', 'test-table-dpco',
    source_profile='public-cloud-prod', target_profile='digital-public-cloudops', clear_table=True)
```

### table_keys(table_name)

table_keys performs a describe on the table and returns the table keys in the following format:

```python
{
    "HASH": HashKeyName,
    "RANGE": RangeKeyName
}
```

If no range key is present, the value for "RANGE" will be None.

### table_key_values(table_name)

table_key_values performs a scan of the table that only returns the values of the keys in the table.  For instance, if you were to perform this on an accounts table where the HASH key is AccountNumber, then it would return a list of dicionaries with the following format:

```python
[{"AccountNumber": "000000000000"}, {"AccountNumber": "000000000001"}, {"AccountNumber": "000000000002"}]
```

[Pypi Deployment](https://pypi.org/project/pynamo/)
