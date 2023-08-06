#!/usr/bin/env python

import asyncio

import aiohttp
from stlib import webapi

session = aiohttp.ClientSession()
loop = asyncio.get_event_loop()

client1 = webapi.SteamWebAPI(session)
client = webapi.Login(session, "laracraft93", "aaaaa")


async def test():
    a = await client1.get_session_id()
    print(a)
    await client.has_phone(a)


loop.run_until_complete(test())
