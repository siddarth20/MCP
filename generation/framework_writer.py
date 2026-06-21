import json
import os
import re


def write_framework(framework):

    framework = framework.strip()

    framework = re.sub(
        r"^```json",
        "",
        framework,
        flags=re.MULTILINE
    )

    framework = re.sub(
        r"^```",
        "",
        framework,
        flags=re.MULTILINE
    )

    framework = framework.strip()

    framework_json = json.loads(
        framework
    )

    files = framework_json.get(
        "files",
        []
    )

    for file_data in files:

        file_name = file_data[
            "name"
        ]

        content = file_data[
            "content"
        ]

        output_path = os.path.join(
            "generated",
            file_name
        )

        os.makedirs(
            os.path.dirname(
                output_path
            ),
            exist_ok=True
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                content
            )

        print(
            f"Generated: {output_path}"
        )