from functions.example.use_cases import hello_use_case


class ExampleController(object):

    def example_get(self, code):
        return hello_use_case(code)
