from pathlib import Path


def save_robot_script(
        filename,
        content):

    Path(
        "generated/robots"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    path = (
        f"generated/robots/"
        f"{filename}.robot"
    )

    with open(
            path,
            "w",
            encoding="utf-8"
    ) as file:

        file.write(content)

    return path