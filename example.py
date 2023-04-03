from qor import Config, Group, Metric, start_server
import click

config = Config(
    [
        Group(
            "Run Info",
            [
                Metric("Date"),
                Metric("Time"),
                Metric("Block_name", rename="Block Name"),
                Metric("Version"),
                Metric("Run"),
                Metric("stage", rename="Stage"),
            ],
            is_run_search=True
        ),
        Group(
            "PPA",
            [
                Metric("Total WNS(ps)", rename="Total WNS (ps)"),
                Metric("total", rename="Total Power (mW)"),
                Metric("Leaf_Cell_Area", rename="Leaf Cell Area (um2)"),
            ]
        ),
        Group(
            "Timing",
            [
                Metric("Total WNS(ps)", reverse=True),
                Metric("Total TNS(ps)", reverse=True),
                Metric("Total FEP"),
                Metric("R2R WNS(ps)", reverse=True),
                Metric("R2R TNS(ps)", reverse=True),
                Metric("R2R FEP"),
            ]
        ),
        Group(
            "Power",
            [
                Metric("internal", rename="Internal Power (mW)"),
                Metric("switching", rename="Switching Power (mW)"),
                Metric("dynamic", rename="Dynamic Power (mW)"),
                Metric("leakage", rename="Leakage Power (mW)"),
                Metric("total", rename="Total Power (mW)"),
            ]
        ),
        Group(
            "Area",
            [
                Metric("X(um)", rename="X (um)"),
                Metric("Y(um)", rename="Y (um)"),
                Metric("Area", rename="Area (um2)"),
                Metric("Leaf_Cell_Area", rename="Leaf Cell Area (um2)"),
                Metric("Utilization"),
            ]
        ),
        Group(
            "Cell Counts",
            [
                Metric("Cell_count", rename="Total Cell Count"),
                Metric("Buf/inv"),
                Metric("Logic"),
                Metric("Flops"),
                Metric("Bits"),
                Metric("Removed_seq"),
                Metric("num_of_ports"),
            ]
        ),
        Group(
            "Vt",
            [
                Metric("%svt"),
                Metric("%lvtll"),
                Metric("%lvt"),
                Metric("%ulvtll"),
                Metric("%ulvt")
            ]
        ),
        Group(
            "Multi Bit",
            [
                Metric("Bank_ratio"), 
                Metric("2_multibit"),
                Metric("4_multibit"),
                Metric("6_multibit"),
                Metric("8_multibit"),
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

@click.command()
@click.option('--csv', help='Name of CSV file to read')
def cli(csv):
    start_server(csv, config)

if __name__ == "__main__":
    cli()