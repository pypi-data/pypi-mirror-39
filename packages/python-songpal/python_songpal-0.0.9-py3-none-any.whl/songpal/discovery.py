@cli.command()
@coro
@click.pass_context
async def discoverng(ctx):
    """Discover supported devices."""
    TIMEOUT = 3
    ST = "urn:schemas-sony-com:service:ScalarWebAPI:1"
    debug = 0
    if ctx.obj:
        debug = ctx.obj["debug"] or 0
    click.echo("Discovering for %s seconds" % TIMEOUT)

    from async_upnp_client import UpnpFactory
    from async_upnp_client.aiohttp import AiohttpRequester

    async def parse_device(device):
        requester = AiohttpRequester()
        factory = UpnpFactory(requester)

        url = device["location"]
        device = await factory.async_create_device(url)

        print(url)

        name = device.name
        udn = device.udn

        print(device._device_description)


        print("name: %s" % device.name)
        print("udn: %s" % device.udn)

        print("got device: %s" % device)
        for service in device.services.values():
            print(service._service_description)

    from async_upnp_client import discovery
    await discovery.async_discover(timeout=TIMEOUT,
                                   service_type=ST,
                                   async_callback=parse_device)