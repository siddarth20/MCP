TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "browser_navigate",
            "description": "Navigate browser to a URL",
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
            "description": "Capture current page structure and state",
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
            "description": "Type text into a field",
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
            "name": "browser_fill_form",
            "description": "Populate multiple form fields",
            "parameters": {
                "type": "object",
                "properties": {
                    "fields": {
                        "type": "array"
                    }
                }
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "browser_click",
            "description": "Click an element",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string"
                    }
                },
                "required": ["target"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "browser_select_option",
            "description": "Select dropdown option",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "browser_hover",
            "description": "Hover element",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "browser_drag",
            "description": "Drag and drop",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "browser_tabs",
            "description": "Manage browser tabs",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "browser_wait_for",
            "description": "Wait for text or condition",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "browser_file_upload",
            "description": "Upload file",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]