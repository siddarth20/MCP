async def discover_tools(session):

    result = await session.list_tools()

    return [
        tool.name
        for tool in result.tools
    ]