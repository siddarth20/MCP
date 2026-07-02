import re


def parse_snapshot(snapshot):

    page = {

        "title": "",

        "url": "",

        "elements": [],

        "texts": [],

        "console": []

    }

    for line in snapshot.splitlines():

        stripped = line.strip()

        if not stripped:

            continue

        if stripped.startswith("- Page URL:"):

            page["url"] = (
                stripped
                .replace(
                    "- Page URL:",
                    ""
                )
                .strip()
            )

            continue

        if stripped.startswith("- Page Title:"):

            page["title"] = (
                stripped
                .replace(
                    "- Page Title:",
                    ""
                )
                .strip()
            )

            continue

        if stripped.startswith("- Console:"):

            page["console"].append(
                stripped
            )

            continue

        ref = re.search(

            r"\[ref=(.*?)\]",

            stripped

        )

        if ref:

            element = {

                "ref":

                    ref.group(1),

                "raw":

                    stripped,

                "type":

                    detect_type(
                        stripped
                    ),

                "label":

                    detect_label(
                        stripped
                    )

            }

            page[
                "elements"
            ].append(
                element
            )

        else:

            if len(stripped) > 2:

                page[
                    "texts"
                ].append(
                    stripped
                )

    return page


def detect_type(line):

    lowered = line.lower()

    mapping = {

        "textbox": "textbox",

        "button": "button",

        "checkbox": "checkbox",

        "radio": "radio",

        "combobox": "dropdown",

        "table": "table",

        "grid": "grid",

        "tree": "tree",

        "dialog": "dialog",

        "menu": "menu",

        "tab": "tab",

        "link": "link",

        "list": "list",

        "textarea": "textarea"

    }

    for key, value in mapping.items():

        if key in lowered:

            return value

    return "unknown"


def detect_label(line):

    match = re.search(

        r'"([^"]+)"',

        line

    )

    if match:

        return match.group(1)

    return ""


def build_context(memory):

    raw = memory.get_context()

    pages = []

    interaction_history = []

    for key, value in raw.items():

        if not key.startswith(
            "browser_snapshot_"
        ):

            continue

        snapshot = value.get(
            "raw",
            ""
        )

        pages.append(
            parse_snapshot(
                snapshot
            )
        )

    for execution in raw.get(

            "execution_history",

            []

    ):

        interaction_history.append(

            {

                "tool":

                    execution.get(
                        "tool"
                    ),

                "args":

                    execution.get(
                        "args",
                        {}
                    ),

                "result":

                    execution.get(
                        "result",
                        {}
                    )

            }

        )

    ui_model = {

        "pages":

            pages,

        "interaction_history":

            interaction_history,

        "tool_history":

            raw.get(

                "tool_history",

                []

            )

    }

    return ui_model