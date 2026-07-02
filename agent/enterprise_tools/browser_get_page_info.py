import json

from agent.enterprise_tools.base_enterprise_tool import (
    EnterpriseTool
)


class BrowserGetPageInfo(
    EnterpriseTool
):

    def __init__(self):

        super().__init__(

            "browser_get_page_info",

            "Returns current page title and URL."

        )

    async def execute(
            self,
            mcp_client,
            arguments):

        javascript = r"""
() => {

    return {

        url: location.href,

        title: document.title

    };

}
"""

        result = await mcp_client.call_tool(

            "browser_evaluate",

            {

                "function": javascript

            }

        )

        if not result.content:

            return {}

        try:

            return json.loads(

                result.content[0].text

            )

        except Exception:

            return {

                "raw": result.content[0].text

            }