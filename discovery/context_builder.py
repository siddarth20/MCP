import re


def extract_elements(snapshot_text):

    elements = []

    textbox_pattern = r'textbox "([^"]+)" \[ref=(.*?)\]'
    button_pattern = r'button "([^"]+)" \[ref=(.*?)\]'
    link_pattern = r'link "([^"]+)" \[ref=(.*?)\]'

    for label, ref in re.findall(
            textbox_pattern,
            snapshot_text):

        elements.append(
            {
                "type": "textbox",
                "label": label,
                "ref": ref
            }
        )

    for label, ref in re.findall(
            button_pattern,
            snapshot_text):

        elements.append(
            {
                "type": "button",
                "label": label,
                "ref": ref
            }
        )

    for label, ref in re.findall(
            link_pattern,
            snapshot_text):

        elements.append(
            {
                "type": "link",
                "label": label,
                "ref": ref
            }
        )

    return elements


def build_context(memory):

    context = memory.get_context()

    pre_snapshot = (
        context.get(
            "browser_snapshot_1",
            {}
        )
    )

    post_snapshot = (
        context.get(
            "browser_snapshot_2",
            {}
        )
    )

    pre_text = (
        pre_snapshot.get(
            "raw",
            ""
        )
    )

    post_text = (
        post_snapshot.get(
            "raw",
            ""
        )
    )

    login_page = (
        context.get(
            "browser_navigate",
            {}
        )
    )

    login_page_text = (
        login_page.get(
            "raw",
            ""
        )
    )

    return {

        "login_page": login_page_text,

        "pre_login_snapshot":
            pre_text,

        "post_login_snapshot":
            post_text,

        "pre_login_elements":
            extract_elements(
                pre_text
            ),

        "post_login_elements":
            extract_elements(
                post_text
            ),

        "tool_history":
            context.get(
                "tool_history",
                []
            ),

        "execution_history":
            context.get(
                "execution_history",
                []
            )
    }