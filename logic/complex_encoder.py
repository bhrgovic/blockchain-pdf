import json
from data.block import Block


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Block):
            return obj.to_dict()  # or your method of serializing a Block
        # Add other types if needed
        return json.JSONEncoder.default(self, obj)