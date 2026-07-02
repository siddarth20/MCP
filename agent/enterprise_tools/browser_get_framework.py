import json

from agent.enterprise_tools.base_enterprise_tool import (
    EnterpriseTool
)


class BrowserGetFramework(
    EnterpriseTool
):

    def __init__(self):

        super().__init__(

            "browser_get_framework",

            "Detect frontend framework."

        )

    async def execute(
            self,
            mcp_client,
            arguments):

        javascript = r"""
() => {

    return {

        angular:
            !!window.ng ||
            !!document.querySelector("[ng-version]"),

        react:
            !!window.__REACT_DEVTOOLS_GLOBAL_HOOK__,

        vue:
            !!window.__VUE__,

        material:
            !!document.querySelector(
                "mat-toolbar,mat-card,mat-form-field"
            ),

        primeng:
            !!document.querySelector(
                "[class*=p-]"
            ),

        bootstrap:
            !!document.querySelector(
                ".container,.row"
            ),

        agGrid:
            !!document.querySelector(
                ".ag-root"
            ),

        kendo:
            !!document.querySelector(
                "[class*=k-grid]"
            ),

        syncfusion:
            !!document.querySelector(
                "[class*=e-grid]"
            )

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