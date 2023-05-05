#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
"""
Grand Entrance Audio Player
(c) Stanley Solutions - 2023
"""
################################################################################

import PySimpleGUI as sg


from GrandEntrance import layout, application, decks

__version__ = "0.0.1"

def entrypoint():
    """Primary Entrypoint for Application."""
    window = sg.Window(
        title=layout.application_title,
        layout=layout.application,
        location=(0,0),
        size=(1200,600),
        resizable=True
    )

    window.finalize()

    # Bind Left/Right/Space
    window.bind('<Right>', '-NEXT-')
    window.bind('<Left>', '-PREVIOUS-')
    window.bind('<space>', '-PLAY-PAUSE-')

    # Build the Deck Manager
    player_deck = decks.PlayerDeck(callback=lambda: window.write_event_value(
        key="-ADVANCE-TRACK-", value=True
    ))

    # Run Main Application
    while not application.main(app=window, player=player_deck):
        continue

    player_deck.active = False # Stop the Player Monitor

    # Remove Window From Screen
    window.close()
