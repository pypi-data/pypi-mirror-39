# pyLivestatus

This package allows to access [Check MK Livestatus](https://mathias-kettner.de/checkmk_livestatus.html) via python

# Usage

```python
from pyLivestatus import Livestatus

livestatus = Livestatus('127.0.0.1', '6557') # host and port of livestatus socket

livestatus.get_hosts() # return array with details for all hosts
livestatus.get_host('my_host') # return details for host 'my_host'
livestatus.get_services('my_host') # return details for every service of host 'my_host'
```
