import re


def classify_element(line):

    element = {
        "type": "unknown",
        "label": "",
        "ref": "",
        "raw": line
    }

    ref_match = re.search(
        r"\[ref=(.*?)\]",
        line
    )

    if ref_match:

        element["ref"] = (
            ref_match.group(1)
        )

    lowered = line.lower()

    mappings = {

        "textbox": "textbox",
        "button": "button",
        "checkbox": "checkbox",
        "radio": "radio",
        "combobox": "dropdown",
        "table": "table",
        "grid": "grid",
        "dialog": "dialog",
        "tab": "tab",
        "menu": "menu",
        "link": "link"
    }

    for key, value in mappings.items():

        if key in lowered:

            element["type"] = value

            break

    label_match = re.search(
        r'"([^"]+)"',
        line
    )

    if label_match:

        element["label"] = (
            label_match.group(1)
        )

    return element


def extract_elements(snapshot):

    elements = []

    for line in snapshot.splitlines():

        if "[ref=" not in line:

            continue

        elements.append(
            classify_element(
                line
            )
        )

    return elements


def build_context(memory):

    raw_context = (
        memory.get_context()
    )

    snapshots = []

    elements = []

    interactions = []

    for key, value in raw_context.items():

        if key.startswith(
                "browser_snapshot_"
        ):

            snapshot = value.get(
                "raw",
                ""
            )

            snapshots.append(
                snapshot
            )

            elements.extend(
                extract_elements(
                    snapshot
                )
            )

    for item in raw_context.get(
            "execution_history",
            []
    ):

        interactions.append(
            {
                "tool":
                    item.get(
                        "tool"
                    ),

                "args":
                    item.get(
                        "args",
                        {}
                    ),

                "result":
                    item.get(
                        "result",
                        {}
                    )
            }
        )

    return {

        "screens":
            snapshots,

        "elements":
            elements,

        "interactions":
            interactions,

        "tool_history":
            raw_context.get(
                "tool_history",
                []
            )
    }