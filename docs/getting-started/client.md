# Using the client

The `Client` class is used to interact with the unkey API. You use
the client to make requests.

## Instantiating the client

```py
import unkey

client = unkey.Client(
    "api_abc123",  # The root api key to use.
    api_version=1,
    api_base_url="https://api.unkey.dev",
)
```

Api version and base url are both optional. The client defaults to api v1
and the production unkey api url. If you are running a local instance of the
api you can set the base url to your instance.

## Handling client resources

The unkey `Client` uses an `aiohttp.ClientSession` under the hood, so
it is important that you call `Client.start` and `Client.close` appropriately.

```py
# ...continued from above

await client.start()

# Make requests here...

await client.close()
```

You will receive errors/warnings if you do not properly starting the client
before using it, or closing it before your program terminates.

## Example client usage

```py
import asyncio
import os

import unkey


async def main() -> None:
    client = unkey.Client(api_key=os.environ["API_KEY"])
    await client.start()

    # 10 requests/second
    ratelimit = unkey.Ratelimit(
        unkey.RatelimitType.Fast,
        limit=10,
        refill_rate=10,
        refill_interval=1000,
    )

    result = await client.keys.create_key(
        os.environ["API_ID"],
        "jonxslays",  # user id
        "test",  # prefix
        byte_length=32,
        ratelimit=ratelimit,
        meta={"is_cool": True},
        expires=9600 * 1000,  # 9600 seconds in the future
    )

    if result.is_ok:
        data = result.unwrap()
        print(data.key_id)
        print(data.key)
    else:
        print(result.unwrap_err())

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

```
