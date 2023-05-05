################################################################################
"""
Grand Entrance Audio Player
(c) Stanley Solutions - 2023
"""
################################################################################

import PySimpleGUI as sg


primary_color = "red"
secondary_color = "yellow"

application_title = "Grand Entrance"

application_bar = [
    ['File', ['Open']]
]

application_body = [
    [
        sg.Table(
            values=[["", ""]],
            headings=["Filename", "Full Path"],
            key="file_list",
            col_widths=[30, 90],
            auto_size_columns=False,
            expand_x=True,
            expand_y=True,
        )
    ]
]

application = [
    [sg.Menu(application_bar)],
    [application_body]
]
