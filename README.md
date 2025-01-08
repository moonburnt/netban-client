# Netban Client

## Description

**Netban** - a moderation tool to restrict users per 'networks' of channels on
social media services. This is an official python client library to connect to
[netban-server](https://github.com/moonburnt/netban-server) instances.

## Dependencies

- python: 3.12
- aiohttp: 3.11
- pydantic: 2.10

## Installation

### With git

```
git clone https://github.com/moonburnt/netban-client.git
cd netban-client
poetry install
```

### From pypi

TODO

## Usage

- Install this library
- Login to admin interface of your netban server instance and create a token
within the "tokens" area.
- Initialize a client like

```python

c = NetbanClient(host_url=host, auth_token=token)

```

where "host_url" is a host+port of your netban server, and "auth_token" is a token
you just created.

- Do whatever you want! (maybe try some code from the 'examples' category down below?)

## Examples

This library is primary meant to be used withing a client implementation.
If you are willing to write your own, or planning to use this somehow else, here
are some usage examples:

### Getting a list of user's restrictions

```python

from src.client import NetbanClient
import asyncio

async def main():
    host = "your_host_plus_port"
    token = "your_token_goes_there"
    user = "id_of_a_user_you_want_to_ban"

    c = NetbanClient(host_url=host, auth_token=token)
    resp = await c.get_restrictions_for_user(
        user = user,
    )
    print(resp)

asyncio.run(main())

```

### Banning a user on your chat group

```python

# Asyncio parts omitted
c = NetbanClient(host_url=host, auth_token=token)
resp = await c.restrict_user(
    user = "user_id",
    restricted_by="moderator_id",
    group = "your_group_id",
)
print(resp)

```

### Running via context manager

```python

# Asyncio parts omitted
async with NetbanClient(host_url=host, auth_token=token) as ctx:
    resp = await ctx.get_restrictions_for_user(
        user = "user_id",
    )
    print(resp)

```



## License

[MIT](https://github.com/moonburnt/netban-client/blob/master/LICENSE)
