import json

from agent.enterprise_tools.base_enterprise_tool import (
    EnterpriseTool
)


class BrowserGetButtons(
    EnterpriseTool
):

    def __init__(self):

        super().__init__(

            "browser_get_buttons",

            "Returns all clickable buttons including icon buttons."

        )

    async def execute(
            self,
            mcp_client,
            arguments):

        javascript = r"""
() => {

    function visible(el){

        return !!(
            el.offsetWidth ||
            el.offsetHeight ||
            el.getClientRects().length
        );

    }

    function attrs(el){

        const obj = {};

        for(const a of el.attributes){

            obj[a.name] = a.value;

        }

        return obj;

    }

    const buttons = [];

    const selectors = [

        "button",

        "[role='button']",

        "input[type=button]",

        "input[type=submit]",

        "input[type=reset]",

        ".btn",

        ".mat-mdc-button",

        ".mat-mdc-raised-button",

        ".mat-mdc-unelevated-button",

        ".mat-mdc-outlined-button",

        ".mat-mdc-icon-button",

        ".mat-mdc-fab",

        ".mat-mdc-mini-fab",

        "mat-icon",

        "mat-icon-button",

        ".p-button",

        "p-button button",

        ".ag-header-cell-menu-button",

        ".ag-icon",

        ".ag-menu-option",

        ".ag-paging-button",

        ".ag-checkbox-input-wrapper",

        "[aria-label]",

        "[title]"

    ];

    const visited = new Set();

    document.querySelectorAll(

        selectors.join(",")

    ).forEach(el => {

        if(visited.has(el))
            return;

        visited.add(el);

        const svg = el.querySelector("svg");

        const icon = el.querySelector(

            "mat-icon,i,span.material-icons"
        );

        const text =

            (el.innerText || "").trim();

        const aria =

            el.getAttribute("aria-label") || "";

        const title =

            el.getAttribute("title") || "";

        buttons.push({

            tag:

                el.tagName.toLowerCase(),

            id:

                el.id || "",

            text:

                text,

            title:

                title,

            ariaLabel:

                aria,

            role:

                el.getAttribute("role") || "",

            visible:

                visible(el),

            enabled:

                !el.disabled,

            classes:

                [...el.classList],

            hasSvg:

                !!svg,

            hasIcon:

                !!icon,

            iconText:

                icon
                    ? icon.innerText.trim()
                    : "",

            tooltip:

                title ||

                aria,

            attributes:

                attrs(el)

        });

    });

    return buttons;

}
"""

        result = await mcp_client.call_tool(

            "browser_evaluate",

            {

                "function": javascript

            }

        )

        if not result.content:

            return []

        text = result.content[0].text

        try:

            return json.loads(text)

        except Exception:

            return {

                "raw": text

            }