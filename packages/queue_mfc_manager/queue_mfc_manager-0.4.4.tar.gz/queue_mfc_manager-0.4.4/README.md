# README 

Simple queue manger for Redis.


## Install

For install manager you need whether to clone this repositori:

```
git clone https://github.com/seregagavrilov/queue_mfc_manager
```

or use pip:

```
pip install queue_mfc_manager
```
## Use                   
You should create file name manager.py and create two necessary instance: "redis" and "manager". 
Then you sholud add tasks to manager.
                  
```
from queue_manager import QManager
from redis import Redis


redis = Redis()
manager = QManager(redis)
manager.add_to_queue(foo, ['a', 1, 'b', 2, 'c', 3])
manager.add_to_queue(bar, ['a', 1, 'b', 2], name='Name')
manager.add_to_queue(say_name, ['name', 'Sergey', 'sourname', 'Gavrilov'])
```
## Run workers
For run workers you need write comand with nomber of workers who will complete your jobs:
```
 workers <number of workers>
```
If you need delete queue from manager use:
```
 deletetasks <queue_name>
```
And that's all! Enjoy!
