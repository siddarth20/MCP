from abc import ABC, abstractmethod


class EnterpriseTool(ABC):

    def __init__(
            self,
            name,
            description):

        self.name = name

        self.description = description

        self.parameters = {

            "type": "object",

            "properties": {

            },

            "additionalProperties": False

        }

    @abstractmethod
    async def execute(
            self,
            session,
            arguments):

        pass