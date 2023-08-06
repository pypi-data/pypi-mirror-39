from json_tricks import dumps


class InstanceForJSON():
    def __init__(self, name, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class QManager():
    def __init__(self, kvstorage):
        self.redis_storage = kvstorage
        self.task_for_workers = {}


    def add_to_queue(self, function, *args, **kwargs):
        try:
            positional_args = args[0]
        except:
            positional_args =[]
        instance = InstanceForJSON(function.__name__, positional_args =positional_args, named_arguments=kwargs)
        self.task_for_workers[function.__name__] = function
        json = self.serialize_to_json(instance)
        self.add_to_qvstorage(function.__name__, json, self.redis_storage)


    def serialize_to_json(self, instance_to_json):
        json = dumps(instance_to_json, indent=4)
        return json


    def add_to_qvstorage(self, function_name, json, kvstor):
        kvstor.lpush(function_name, json)


    def take_from_qvstorage(self, function_name, kvstor):
        return kvstor.rpop(function_name)
