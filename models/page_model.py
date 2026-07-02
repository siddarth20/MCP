from dataclasses import dataclass, field


@dataclass
class FrameworkInfo:

    angular: bool = False

    react: bool = False

    vue: bool = False

    material: bool = False

    primeng: bool = False

    bootstrap: bool = False

    ag_grid: bool = False

    kendo: bool = False

    syncfusion: bool = False


@dataclass
class PageModel:

    #
    # Basic page information
    #

    url: str = ""

    title: str = ""

    snapshot: str = ""

    framework: FrameworkInfo = field(

        default_factory=FrameworkInfo

    )

    #
    # UI Components
    #

    inputs: list = field(default_factory=list)

    buttons: list = field(default_factory=list)

    forms: list = field(default_factory=list)

    tables: list = field(default_factory=list)

    dropdowns: list = field(default_factory=list)

    dialogs: list = field(default_factory=list)

    links: list = field(default_factory=list)

    svg_icons: list = field(default_factory=list)

    date_pickers: list = field(default_factory=list)

    tabs: list = field(default_factory=list)

    accordions: list = field(default_factory=list)

    cards: list = field(default_factory=list)

    menus: list = field(default_factory=list)

    #
    # Diagnostics
    #

    console_messages: list = field(

        default_factory=list

    )

    network_requests: list = field(

        default_factory=list

    )

    #
    # History
    #

    execution_history: list = field(

        default_factory=list

    )