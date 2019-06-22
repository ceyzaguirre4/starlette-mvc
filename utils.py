import asyncio

def asyncify(func):
    async def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        func_out = await loop.run_in_executor(None, func, *args, **kwargs)
        return func_out
    return inner
