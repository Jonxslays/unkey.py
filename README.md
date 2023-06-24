# unkey.py

An asynchronous Python SDK for [unkey.dev](https://unkey.dev/).

## Installation

**Python version 3.8 or greater is required to use unkey.py.**

### Stable

```sh
pip install -U unkey.py
```

### Development

```sh
pip install -U git+https://github.com/Jonxslays/unkey.py
```

For more information on using `pip`, check out the [pip documentation](https://pip.pypa.io/en/stable/).

## Example

```py
import asyncio
import os

import unkey


async def main() -> None:
    client = unkey.Client(api_key=os.environ["API_KEY"])
    await client.start()

    result = await client.keys.create_key(
        os.environ["API_ID"], "jonxslays", "test"
    )

    if result.is_ok:
        data = result.unwrap()
        print(data.id)
        print(data.key)
    else:
        print(result.unwrap_err())

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

```

## What is unkey.dev

unkey.dev is a fully open source API key management solution. It allows you to create,
manage, and validate API keys for your applications users. You can even host it yourself,
that's the beauty of open source.

If you're interested in learning more about the project, consider checking out any of these links:

- [Website](https://unkey.dev/)
- [API documentation](https://docs.unkey.dev/)
- [Github repository](https://github.com/chronark/unkey)
- [Discord community](https://discord.gg/TmMczTKArw)

## Contributing

unkey.py is open to contributions. Check out the
[contributing guide](https://github.com/Jonxslays/unkey.py/blob/master/CONTRIBUTING.md) to learn how.

## License

unkey.py is licensed under the [GPLv3 License](https://github.com/Jonxslays/unkey.py/blob/master/LICENSE).
