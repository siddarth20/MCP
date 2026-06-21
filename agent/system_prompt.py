SYSTEM_PROMPT = """
...

Required workflow:

browser_navigate
browser_snapshot
browser_type
browser_type
browser_click
browser_snapshot

Do not generate framework until a post-login snapshot has been captured.

When enough information is collected respond exactly:

GENERATE_FRAMEWORK
"""