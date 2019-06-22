# Starlette MVC

A barebones template for using [Starlette](https://www.starlette.io) in real world usecases.
The motivation behind this was that no real starlette usage examples were available.
This template showcases most Starlette functionality and adds some new ones, such as async user authetication via JWT cookies and BCrypt.


### async bcrypt for authentification

Thanks to its C backend, bcrypt can be run efficiently with threads (as it releases the GIL for most of the processing). 
For this reason, we can use bcrypt asynchronously by using the default thread pool with `loop.run_in_executor(None, bcrypt_foo)`.
This is implemented in a wrapper (`@asyncify`) in [utils.py](utils.py).

~~~python
import bcrypt

def test_pass():
    return bcrypt.hashpw("some password".encode('utf-8'), bcrypt.gensalt())

# slow
result = [test_pass() for _ in range(100)]

# 10 times faster
tasks = asyncio.gather(*[loop.run_in_executor(None, test_pass) for _ in range(100)])
result = await tasks
~~~

\#(the same was implemented for password checking but not for JWT generating since the overhead added by generating the tokens is minimal).
