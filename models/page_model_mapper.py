class PageModelMapper:

    @staticmethod
    def update(
            page_model,
            tool_name,
            result):

        #
        # Keep execution history
        #

        page_model.execution_history.append(

            {

                "tool": tool_name,

                "result": result

            }

        )

        #
        # Snapshot
        #

        if tool_name == "browser_snapshot":

            page_model.snapshot = result.get(

                "raw",

                ""

            )

            return

        #
        # Page Information
        #

        if tool_name == "browser_get_page_info":

            page_model.url = result.get(

                "url",

                ""

            )

            page_model.title = result.get(

                "title",

                ""

            )

            return

        #
        # Framework
        #

        if tool_name == "browser_get_framework":

            page_model.framework.angular = result.get(

                "angular",

                False

            )

            page_model.framework.react = result.get(

                "react",

                False

            )

            page_model.framework.vue = result.get(

                "vue",

                False

            )

            page_model.framework.material = result.get(

                "material",

                False

            )

            page_model.framework.primeng = result.get(

                "primeng",

                False

            )

            page_model.framework.bootstrap = result.get(

                "bootstrap",

                False

            )

            page_model.framework.ag_grid = result.get(

                "agGrid",

                False

            )

            page_model.framework.kendo = result.get(

                "kendo",

                False

            )

            page_model.framework.syncfusion = result.get(

                "syncfusion",

                False

            )

            return

        #
        # Controls
        #

        if tool_name == "browser_get_inputs":

            page_model.inputs = result

            return

        if tool_name == "browser_get_buttons":

            page_model.buttons = result

            return

        if tool_name == "browser_get_forms":

            page_model.forms = result

            return

        if tool_name == "browser_get_tables":

            page_model.tables = result

            return

        if tool_name == "browser_get_dropdowns":

            page_model.dropdowns = result

            return

        if tool_name == "browser_get_dialogs":

            page_model.dialogs = result

            return

        if tool_name == "browser_get_links":

            page_model.links = result

            return

        if tool_name == "browser_get_svg_icons":

            page_model.svg_icons = result

            return

        if tool_name == "browser_get_datepickers":

            page_model.date_pickers = result

            return

        if tool_name == "browser_get_tabs":

            page_model.tabs = result

            return

        if tool_name == "browser_get_accordions":

            page_model.accordions = result

            return

        if tool_name == "browser_get_cards":

            page_model.cards = result

            return

        if tool_name == "browser_get_menus":

            page_model.menus = result

            return

        #
        # Diagnostics
        #

        if tool_name == "browser_console_messages":

            page_model.console_messages = result

            return

        if tool_name == "browser_network_requests":

            page_model.network_requests = result

            return