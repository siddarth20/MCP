import json


class DOMAnalyzer:

    def __init__(self):
        pass

    async def analyze(
            self,
            session):

        javascript = r"""
() => {

    function attrs(element){

        const obj = {};

        for(const a of element.attributes){

            obj[a.name] = a.value;

        }

        return obj;

    }

    function visible(el){

        return !!(

            el.offsetWidth ||

            el.offsetHeight ||

            el.getClientRects().length

        );

    }

    function xpath(el){

        if(el.id){

            return '//*[@id="' + el.id + '"]';

        }

        if(el===document.body){

            return "/html/body";

        }

        let ix = 0;

        const siblings = el.parentNode.childNodes;

        for(let i=0;i<siblings.length;i++){

            const sibling = siblings[i];

            if(sibling===el){

                return xpath(el.parentNode)+"/"+el.tagName.toLowerCase()+"["+(ix+1)+"]";

            }

            if(

                sibling.nodeType===1 &&

                sibling.tagName===el.tagName

            ){

                ix++;

            }

        }

    }

    const controls=[];

    document.querySelectorAll("*").forEach(el=>{

        controls.push({

            tag:el.tagName.toLowerCase(),

            id:el.id||"",

            name:el.getAttribute("name")||"",

            type:el.getAttribute("type")||"",

            role:el.getAttribute("role")||"",

            placeholder:el.getAttribute("placeholder")||"",

            title:el.getAttribute("title")||"",

            text:(el.innerText||"").trim(),

            value:el.value||"",

            visible:visible(el),

            enabled:!el.disabled,

            required:!!el.required,

            classes:[...el.classList],

            attributes:attrs(el),

            xpath:xpath(el)

        });

    });

    return {

        url:location.href,

        title:document.title,

        html:document.documentElement.outerHTML,

        controls:controls

    };

}
"""

        result = await session.call_tool(

            "browser_evaluate",

            {

                "function": javascript

            }

        )

        if not result.content:

            return {

                "success":False,

                "error":"No response."

            }

        text = result.content[0].text

        try:

            return json.loads(text)

        except Exception:

            return {

                "raw":text

            }