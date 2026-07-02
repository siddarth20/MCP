import json

from agent.enterprise_tools.base_enterprise_tool import (
    EnterpriseTool
)


class BrowserGetForms(
    EnterpriseTool
):

    def __init__(self):

        super().__init__(

            "browser_get_forms",

            "Returns all forms and their controls."

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

    const forms = [];

    document.querySelectorAll("form").forEach(form => {

        const controls = [];

        form.querySelectorAll(

            "input,textarea,select,button"

        ).forEach(control => {

            controls.push({

                tag:
                    control.tagName.toLowerCase(),

                id:
                    control.id || "",

                name:
                    control.name || "",

                type:
                    control.type || "",

                role:
                    control.getAttribute("role") || "",

                placeholder:
                    control.placeholder || "",

                text:
                    (control.innerText || "").trim(),

                title:
                    control.title || "",

                ariaLabel:
                    control.getAttribute("aria-label") || "",

                required:
                    !!control.required,

                disabled:
                    !!control.disabled,

                readonly:
                    !!control.readOnly,

                visible:
                    visible(control),

                classes:
                    [...control.classList],

                attributes:
                    attrs(control)

            });

        });

        forms.push({

            id:
                form.id || "",

            name:
                form.getAttribute("name") || "",

            action:
                form.action || "",

            method:
                form.method || "GET",

            autocomplete:
                form.autocomplete || "",

            noValidate:
                form.noValidate,

            visible:
                visible(form),

            classes:
                [...form.classList],

            attributes:
                attrs(form),

            controlCount:
                controls.length,

            controls:
                controls

        });

    });

    return forms;

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