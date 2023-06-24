from unkey import Client


def test_placeholder() -> None:
    client = Client(":eyes:")
    assert isinstance(client, Client)
