import asyncio


# This is not a real coroutine since it doesn't pause
# the execution of a programme using await
async def square(number):
    return number * number


async def main():

    # Pauses execution of a function
    # Useful with long-running operations, because you can
    # run other code
    x = await square(10)
    print(f"x = {x}")

    y = await square(5)
    print(f"y = {y}")

    print(f"sum = {x + y}")


if __name__ == "__main__":
    # Calling coroutine doesn't execute it immediately
    # You need to run it in an event loop provided by asyncio module
    # result = square(10)
    # print(square)

    # asyncio.run(square(10))

    asyncio.run(main())
