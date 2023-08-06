#
# Module contain manager class which work with kv storage
#
# Copyright (c) 2018, Gavrilov S
# Licensed MIT License.
#


from json_tricks import dumps
from redis import Redis


class Json:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class QManager:
    def __init__(self, redis):
        if redis.__class__ == Redis:
            self._redis = redis
        else:
            raise TypeError('You can define only redis object')

        self._queue_name = 'tasks'
        self._task_for_workers = {}

    @staticmethod
    def __serialize_to_json(object_for_json):
        json = dumps(object_for_json, indent=4)
        return json

    def define_queue_name(self, name):
        self._queue_name = name

    def add_to_queue(self, task, *args, **kwargs):
        instance = Json(function_name=task.__name__,
                        arguments={'positional': args, 'keyword': kwargs}
                        )
        json = self.__serialize_to_json(instance)
        self._task_for_workers[task.__name__] = task
        self._redis.rpush(self._queue_name, json)

    def get_task(self, task_name):
        return self._task_for_workers[task_name]

    def get_redis_object(self):
        return self._redis

    def delete_all_tasks(self, key=None):
        if key:
            self._redis.delete(key)
        else:
            self._redis.delete('tasks')

    def take_from_queue(self):
        return self._redis.lpop(self._queue_name)