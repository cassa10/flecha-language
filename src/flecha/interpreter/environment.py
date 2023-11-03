
class GlobalEnvironment:
    def __init__(self):
        self.globals = {}

    def extend(self, _id, val):
        self.globals[_id] = val
        return self

    def lookup(self, _id):
        try:
            return self.globals[_id]
        except:
            raise RuntimeError(f'Id {_id} not defined')


class LocalEnvironment:

    def __init__(self, stack_frame=None):
        if stack_frame is None:
            stack_frame = []
        self.stack_frame = stack_frame

    def extend(self, _id, val):
        return LocalEnvironment([(_id, val)] + self.stack_frame)

    def lookup(self, _id1):
        return next((val for _id2, val in self.stack_frame if _id2 == _id1), None)

