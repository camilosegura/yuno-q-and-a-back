class Hello(object):
    # Dependencie Injection
    def __init__(self, hello_msg: str):
        self._hello_msg = hello_msg

    def execute(self, code: str):
        return {"msg": f"{self._hello_msg} code {code}"}
