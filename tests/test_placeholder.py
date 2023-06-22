from unkey import Client


def test_placeholder() -> None:
    client = Client()
    assert isinstance(client, Client)
