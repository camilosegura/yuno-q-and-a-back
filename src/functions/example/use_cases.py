from .hello import Hello
from os import getenv

_HELLO_MSG = getenv("HELLO_MSG", "Hi there")

hello_use_case = Hello(hello_msg=_HELLO_MSG).execute
