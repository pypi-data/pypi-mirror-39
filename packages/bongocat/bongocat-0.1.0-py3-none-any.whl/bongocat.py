
"""generic bongocat-like overlay

Usage:
    bongocat [--images=<path>] [--neutral=<name>]
    bongocat -h | --help

Options:
    -h --help           Show this screen
    --images=<path>     Leading to folder for assets
    --neutral=<name>    Represents the no-state image [default: -]
"""

import sys, os
import itertools
import tkinter


__version__ = '0.1.0'

__all__ = ()


def construct():

    root = tkinter.Tk()

    root.title(__version__)

    label = tkinter.Label(root)

    return (root, label)


def load(default, path):

    from PIL import (Image, ImageTk)

    directory = os.path.join(os.getcwd(), path)

    (photos, states) = ([], [])

    extensions = ('png', 'jpg')

    for entry in os.scandir(path = directory):

        if not entry.is_file():

            continue

        try:

            (text, extension) = entry.name.rsplit('.', 1)

        except ValueError:

            continue

        if not extension in extensions:

            continue

        states.append(text.lower())

        image = Image.open(entry.path)

        photo = ImageTk.PhotoImage(image)

        photos.append(photo)

    try:

        index = states.index(default)

    except ValueError:

        message = 'Missing file "{0}" for neutral state.'.format(default)

        raise ValueError(message) from None

    del states[index]

    neutral = photos.pop(index)

    responses = {}

    for (photo, state) in zip(photos, states):

        combos = itertools.permutations(state, len(state))

        for combo in map(''.join, combos):

            responses[combo] = photo

    assets = (neutral, responses)

    return assets


def apply(label, neutral, responses):

    import keyboard

    active = set()

    def analyse():

        if active:

            state = ''.join(active)

            try:

                response = responses[state]

            except KeyError:

                return

        else:

            response = neutral

        label.configure(image = response)

    def switch(key):

        if key in active:

            return

        active.add(key)

        analyse()

    def revert(key):

        try:

            active.remove(key)

        except KeyError:

            return

        analyse()

    def attach(function):

        def wrapper(event):

            function(event.name)

        return wrapper

    binders = (keyboard.on_press_key, keyboard.on_release_key)

    handlers = map(attach, (switch, revert))

    for (binder, handler) in zip(binders, handlers):

        for key in responses.keys():

            try:

                binder(key, handler)

            except ValueError:

                continue


def start():

    import docopt

    arguments = docopt.docopt(__doc__)

    (root, label) = construct()

    default = arguments['--neutral']

    path = arguments['--images']

    (neutral, responses) = load(default, path if path else '')

    label.configure(image = neutral)

    apply(label, neutral, responses)

    label.pack()

    try:

        root.mainloop()

    except KeyboardInterrupt:

        pass

if __name__ == '__main__':

    start()
