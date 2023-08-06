pysignald
=======

[![pipeline status](https://gitlab.com/stavros/pysignald/badges/master/pipeline.svg)](https://gitlab.com/stavros/pysignald/commits/master)

pysignald is a Python client for the excellent [signald](https://git.callpipe.com/finn/signald) project, which in turn
is a command-line client for the Signal messaging service.

pysignald allows you to programmatically send and receive messages to Signal.

Installation
------------

You can install pysignald with pip:

```
$ pip install pysignald
```


Running
-------

Just make sure you have signald installed. Here's an example of how to use pysignald:


```python
from signald import Signal

s = Signal("+1234567890")
s.send_message("+1098765432", "Hello there!")

for message in s.receive_messages():
    print(message)
```
