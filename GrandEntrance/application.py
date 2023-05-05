################################################################################
"""
Grand Entrance Audio Player
(c) Stanley Solutions - 2023
"""
################################################################################

import os

import PySimpleGUI as sg

from GrandEntrance import decks, layout

previous = 0

def update_colors(app: sg.Window, previous: int, active: int):
    """Update the Row Colors."""
    app['file_list'].update(
        row_colors=[
            (previous, layout.secondary_color, "black"),
            (active, layout.primary_color, "black"),
        ]
    )

def main(app: sg.Window, player: decks.PlayerDeck) -> bool:
    """Core Application Graphical Interface."""
    global previous

    # Get Application Values
    event, values = app.read()

    # App Close?
    if event == sg.WINDOW_CLOSED:
        return True # Complete!
    elif event == "Open":
        # Load the File List
        files = list(sg.popup_get_file(
            message="Select Grand Entrance Audio Files",
            title="Select Audio Files",
            multiple_files=True,
            initial_folder=os.path.join(os.path.expanduser('~'), 'Music'),
            file_types=(
                ('MP3', '*.mp3'),
                ('WAV', '*.wav'),
                ('FLAC', '*.flac'),
            ),
            no_window=True,
        ))
        app['file_list'].update(
            values=[[os.path.basename(path), path] for path in files],
            row_colors=[(player.active_index, layout.secondary_color, "black")]
        )
        player.load_playlist(files)
    elif event == "-NEXT-":
        player.stop()
        player.next()
        update_colors(app=app, previous=previous, active=player.active_index)
    elif event == "-PREVIOUS-":
        player.stop()
        player.previous()
        update_colors(app=app, previous=previous, active=player.active_index)
    elif event == "-PLAY-PAUSE-":
        player.play_stop()
        update_colors(app=app, previous=previous, active=player.active_index)
    elif event == "-ADVANCE-TRACK-":
        update_colors(app=app, previous=previous, active=player.active_index)
    else:
        print("Undefined Event!")
        print(event)
        print(values)
    
    previous = player.active_index
