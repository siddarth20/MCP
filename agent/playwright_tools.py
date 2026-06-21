TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "browser_navigate",
            "description": "Navigate to URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string"
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browser_snapshot",
            "description": "Capture page snapshot",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browser_type",
            "description": "Type text into element",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string"
                    },
                    "text": {
                        "type": "string"
                    }
                },
                "required": [
                    "target",
                    "text"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browser_click",
            "description": "Click element",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string"
                    }
                },
                "required": [
                    "target"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "browser_wait_for",
            "description": "Wait for text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string"
                    }
                },
                "required": [
                    "text"
                ]
            }
        }
    }
]