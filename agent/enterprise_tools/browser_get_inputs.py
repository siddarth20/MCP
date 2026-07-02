import json

from agent.enterprise_tools.base_enterprise_tool import (
    EnterpriseTool
)


class BrowserGetInputs(
    EnterpriseTool
):

    def __init__(self):

        super().__init__(

            "browser_get_inputs",

            "Returns all editable input controls on the current page."

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

    const inputs = [];

    const selectors = [

        "input",

        "textarea",

        "mat-form-field input",

        "mat-select",

        "mat-datepicker",

        "p-inputtext",

        "p-password input",

        "p-calendar input",

        "p-inputnumber input",

        "p-autocomplete input",

        "input[type=text]",

        "input[type=password]",

        "input[type=email]",

        "input[type=number]",

        "input[type=search]",

        "input[type=date]",

        "input[type=datetime-local]",

        "input[type=tel]",

        "input[type=url]"

    ];

    document.querySelectorAll(

        selectors.join(",")

    ).forEach(el => {

        inputs.push({

            tag:
                el.tagName.toLowerCase(),

            id:
                el.id || "",

            name:
                el.name || "",

            type:
                el.type || "",

            role:
                el.getAttribute("role") || "",

            placeholder:
                el.placeholder || "",

            value:
                el.value || "",

            text:
                (el.innerText || "").trim(),

            title:
                el.title || "",

            ariaLabel:
                el.getAttribute("aria-label") || "",

            visible:
                visible(el),

            enabled:
                !el.disabled,

            required:
                !!el.required,

            readonly:
                !!el.readOnly,

            classes:
                [...el.classList],

            attributes:
                attrs(el)

        });

    });

    return inputs;

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