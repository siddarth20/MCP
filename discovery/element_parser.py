import re


def parse_snapshot(snapshot_text):

    elements = []

    textbox_pattern = (
        r'textbox\s+"([^"]+)"\s+\[ref=(.*?)\]'
    )

    button_pattern = (
        r'button\s+"([^"]+)"\s+\[ref=(.*?)\]'
    )

    link_pattern = (
        r'link\s+"([^"]+)"\s+\[ref=(.*?)\]'
    )

    for match in re.finditer(
            textbox_pattern,
            snapshot_text):

        elements.append(
            {
                "type": "textbox",
                "label": match.group(1),
                "ref": match.group(2)
            }
        )

    for match in re.finditer(
            button_pattern,
            snapshot_text):

        elements.append(
            {
                "type": "button",
                "label": match.group(1),
                "ref": match.group(2)
            }
        )

    for match in re.finditer(
            link_pattern,
            snapshot_text):

        elements.append(
            {
                "type": "link",
                "label": match.group(1),
                "ref": match.group(2)
            }
        )

    return elements