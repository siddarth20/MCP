def build_optimized_dom_script(
        tool_args):

    tool_args = tool_args or {}

    max_depth = int(
        tool_args.get(
            "max_depth",
            20
        )
    )

    max_nodes = int(
        tool_args.get(
            "max_nodes",
            400
        )
    )

    include_hidden = bool(
        tool_args.get(
            "include_hidden",
            False
        )
    )

    javascript = r"""
() => {

    const MAX_DEPTH = __MAX_DEPTH__;
    const MAX_NODES = __MAX_NODES__;
    const INCLUDE_HIDDEN = __INCLUDE_HIDDEN__;
    const MAX_TEXT = 120;

    let nodeCount = 0;
    let truncated = false;

    const SKIP_TAGS = new Set([
        "script", "style", "noscript", "template",
        "link", "meta", "svg", "path", "br", "wbr"
    ]);

    const INTERACTIVE_TAGS = new Set([
        "a", "button", "input", "select", "textarea",
        "option", "label"
    ]);

    const CLICKABLE_ROLES = new Set([
        "button", "link", "checkbox", "radio", "tab",
        "menuitem", "switch", "option"
    ]);

    const ATTR_KEYS = [
        "id", "name", "type", "href", "placeholder",
        "title", "alt"
    ];

    function visible(el) {

        const style = getComputedStyle(el);

        if (
            style.display === "none" ||
            style.visibility === "hidden" ||
            el.getAttribute("aria-hidden") === "true"
        ) {
            return false;
        }

        return !!(
            el.offsetWidth ||
            el.offsetHeight ||
            el.getClientRects().length
        );

    }

    function ownText(el) {

        let text = "";

        for (const node of el.childNodes) {

            if (node.nodeType === Node.TEXT_NODE) {
                text += node.textContent;
            }

        }

        text = text.replace(/\s+/g, " ").trim();

        if (text.length > MAX_TEXT) {
            text = text.slice(0, MAX_TEXT) + "...";
        }

        return text;

    }

    function isInteractive(el) {

        const tag = el.tagName.toLowerCase();
        const role = (el.getAttribute("role") || "").toLowerCase();

        return (
            INTERACTIVE_TAGS.has(tag) ||
            CLICKABLE_ROLES.has(role) ||
            el.hasAttribute("onclick") ||
            (
                el.hasAttribute("tabindex") &&
                el.getAttribute("tabindex") !== "-1"
            )
        );

    }

    function attr(el, name) {
        return el.getAttribute(name) || "";
    }

    function hasMeaningfulAttrs(el) {

        return (
            ATTR_KEYS.some(a => attr(el, a) !== "") ||
            attr(el, "aria-label") !== ""
        );

    }

    function walk(el, depth) {

        if (nodeCount >= MAX_NODES) {
            truncated = true;
            return null;
        }

        const tag = el.tagName.toLowerCase();

        if (SKIP_TAGS.has(tag)) {
            return null;
        }

        if (!INCLUDE_HIDDEN && !visible(el)) {
            return null;
        }

        const children = [];

        if (depth < MAX_DEPTH) {

            for (const child of el.children) {

                const mapped = walk(child, depth + 1);

                if (mapped) {
                    children.push(mapped);
                }

            }

        }

        const text = ownText(el);
        const interactive = isInteractive(el);
        const meaningfulAttrs = hasMeaningfulAttrs(el);

        //
        // Collapse pure wrapper elements: exactly one child,
        // no own text, no meaningful attributes, not interactive.
        //

        if (
            children.length === 1 &&
            text === "" &&
            !interactive &&
            !meaningfulAttrs
        ) {
            return children[0];
        }

        //
        // Drop empty, non-interactive, attribute-less leaves.
        //

        if (
            children.length === 0 &&
            text === "" &&
            !interactive &&
            !meaningfulAttrs
        ) {
            return null;
        }

        const node = { tag: tag };

        const id = attr(el, "id");
        const name = attr(el, "name");
        const type = attr(el, "type");
        const href = attr(el, "href");
        const placeholder = attr(el, "placeholder");
        const title = attr(el, "title");
        const alt = attr(el, "alt");
        const ariaLabel = attr(el, "aria-label");
        const role = attr(el, "role");

        const rawValue = (el.value !== undefined)
            ? String(el.value)
            : "";

        if (id) node.id = id;
        if (name) node.name = name;
        if (type) node.type = type;
        if (href) node.href = href;
        if (placeholder) node.placeholder = placeholder;
        if (rawValue) node.value = rawValue.slice(0, MAX_TEXT);
        if (title) node.title = title;
        if (alt) node.alt = alt;
        if (ariaLabel) node.ariaLabel = ariaLabel;
        if (role) node.role = role;
        if (text) node.text = text;
        if (interactive) node.interactive = true;
        if (el.disabled) node.disabled = true;
        if (el.required) node.required = true;
        if (el.checked) node.checked = true;

        if (children.length) {
            node.children = children;
        }

        nodeCount += 1;

        return node;

    }

    const tree = walk(document.body, 0);

    return {
        tree: tree,
        nodeCount: nodeCount,
        truncated: truncated
    };

}
"""

    javascript = (

        javascript

        .replace(
            "__MAX_DEPTH__",
            str(max_depth)
        )

        .replace(
            "__MAX_NODES__",
            str(max_nodes)
        )

        .replace(
            "__INCLUDE_HIDDEN__",
            "true" if include_hidden else "false"
        )

    )

    return javascript