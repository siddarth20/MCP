SYSTEM_PROMPT = """
...

Required workflow:

browser_navigate
browser_get_optimized_dom
browser_type
browser_type
browser_click
browser_get_optimized_dom

Do not generate framework until a post-login snapshot has been captured.

browser_get_optimized_dom is also available: use it when you need the
full page structure without the noise of raw HTML (it returns a pruned
DOM tree instead).

When enough information is collected respond exactly:

GENERATE_FRAMEWORK
"""