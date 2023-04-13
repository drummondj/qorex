from qor import Config, Group, Metric
import pandas as pd

CONFIG = Config(
    [
        Group(
            "Run Info",
            [
                Metric("Timestamp", derive=lambda x: pd.to_datetime(x.Date + " " + x.Time)),
                Metric("Date"),
                Metric("Time"),
                Metric("Design"),
                Metric("Version"),
                Metric("Run"),
                Metric("stage", rename="Stage"),
            ],
            is_run_search=True
        ),
        Group(
            "Timing",
            [
                Metric("All WNS (ps)", reverse=True),
                Metric("All TNS (ps)", reverse=True),
                Metric("All Violations"),
                Metric("reg2reg WNS (ps)", reverse=True),
                Metric("reg2reg TNS (ps)", reverse=True),
                Metric("reg2reg Violations"),
            ]
        ),
        Group(
            "Power",
            [
                Metric("internal_power", rename="Internal Power (mW)"),
                Metric("switching_power", rename="Switching Power (mW)"),
                Metric("dynamic_power", rename="Dynamic Power (mW)"),
                Metric("leakage_power", rename="Leakage Power (mW)"),
                Metric("total_power", rename="Total Power (mW)"),
            ]
        ),
        Group(
            "Area",
            [
                Metric("X(um)", rename="X (um)"),
                Metric("Y(um)", rename="Y (um)"),
                Metric("Area", rename="Area (um2)"),
                Metric("Cell Area", rename="Leaf Cell Area (um2)"),
                Metric("Utilization"),
            ]
        ),
        Group(
            "Stats",
            [
                Metric("Run_time", rename="Runtime"),
                Metric("CPU"),
                Metric("Mem"),
            ]
        ),
        Group(
            "Hidden",
            [
                Metric("Source"),
            ],
            is_hidden=True
        )
    ]
)
