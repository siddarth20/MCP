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
    },

    {
        "type": "function",
        "function": {
            "name": "browser_get_optimized_dom",
            "description": "Returns the entire page as a pruned, token-efficient DOM tree instead of raw HTML. Hidden elements, empty nodes and purely-structural wrapper elements (e.g. layout divs with a single child and no attributes) are stripped out. Each remaining node keeps only its tag, own visible text, ARIA role and a small set of relevant attributes (id, name, type, href, placeholder, value, title, alt, aria-label) plus interactive/disabled/required/checked flags. Use this to understand the full page structure without the noise of raw HTML.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_depth": {
                        "type": "integer",
                        "description": "Maximum tree depth to walk. Defaults to 20."
                    },
                    "max_nodes": {
                        "type": "integer",
                        "description": "Maximum number of nodes to return before truncating. Defaults to 400."
                    },
                    "include_hidden": {
                        "type": "boolean",
                        "description": "Include hidden elements (display:none, visibility:hidden, zero size, aria-hidden). Defaults to false."
                    }
                }
            }
        }
    }
]