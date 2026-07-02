import json
import os
from pathlib import Path


class FrameworkWriter:

    def __init__(self):

        self.project_root = Path(
            "generated_framework"
        )

    def write(
            self,
            framework):

        if isinstance(
                framework,
                str):

            framework = json.loads(
                framework
            )

        self.create_structure()

        self.write_files(
            framework.get(
                "tests",
                []
            ),
            "tests"
        )

        self.write_files(
            framework.get(
                "pages",
                []
            ),
            "pages"
        )

        self.write_files(
            framework.get(
                "resources",
                []
            ),
            "resources"
        )

        self.write_files(
            framework.get(
                "variables",
                []
            ),
            "variables"
        )

        self.write_files(
            framework.get(
                "keywords",
                []
            ),
            "keywords"
        )

        print()

        print("=" * 80)

        print(
            "Framework generated successfully."
        )

        print(
            self.project_root.absolute()
        )

        print("=" * 80)

    def create_structure(self):

        folders = [

            "tests",

            "pages",

            "resources",

            "variables",

            "keywords",

            "results"

        ]

        self.project_root.mkdir(

            exist_ok=True

        )

        for folder in folders:

            (

                self.project_root /

                folder

            ).mkdir(

                parents=True,

                exist_ok=True

            )

    def write_files(
            self,
            files,
            folder):

        for file in files:

            name = file.get(
                "name"
            )

            content = file.get(
                "content",
                ""
            )

            if not name:

                continue

            path = (

                self.project_root /

                folder /

                name

            )

            path.parent.mkdir(

                parents=True,

                exist_ok=True

            )

            with open(

                    path,

                    "w",

                    encoding="utf-8"

            ) as fp:

                fp.write(
                    content
                )

            print(
                f"Generated {path}"
            )