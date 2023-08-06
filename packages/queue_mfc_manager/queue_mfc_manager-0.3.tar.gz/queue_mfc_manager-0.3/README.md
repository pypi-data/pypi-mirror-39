# README 

Introduce simple manager for manage queue fundamental on Radis.


## Installing

For install this manager you need whether to clone this repositori:

```
git clone https://github.com/seregagavrilov/queue_mfc_manager
```

or install through PIP:

```
pip install queue_mfc_manager
```
## Using                    
for using takes create file name "manager" and create two necessary instance: "redis" and "manager".
                  
```
from queue_manager import QManager
from redis import Redis


redis = Redis()
manager = QManager(redis)
manager.add_to_queue(foo, ['a', 1, 'b', 2, 'c', 3])
manager.add_to_queue(bar, ['a', 1, 'b', 2], name='Name')
manager.add_to_queue(say_name, ['name', 'Sergey', 'sourname', 'Gavrilov'])
```
## Launch workers
For launch workers you need write comand with nomber of workers who will complete your jobs:
```
 workers 4
```
And that's all! Enjoy!