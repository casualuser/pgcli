#!/usr/bin/env python
"""
An example of how to deal with slow auto completion code.

- Running the completions in a thread is possible by wrapping the
  `Completer` object in a `ThreadedCompleter`. This makes sure that the
  ``get_completions`` generator is executed in a background thread.

  For the `prompt` shortcut, we don't have to wrap the completer ourselves.
  Passing `complete_in_thread=True` is sufficient.

- We also set a `loading` boolean in the completer function to keep track of
  when the completer is running, and display this in the toolbar.
"""
from __future__ import unicode_literals

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.shortcuts import prompt, CompleteStyle
import time

WORDS = [
    'alligator', 'ant', 'ape', 'bat', 'bear', 'beaver', 'bee', 'bison',
    'butterfly', 'cat', 'chicken', 'crocodile', 'dinosaur', 'dog', 'dolphin',
    'dove', 'duck', 'eagle', 'elephant', 'fish', 'goat', 'gorilla', 'kangaroo',
    'leopard', 'lion', 'mouse', 'rabbit', 'rat', 'snake', 'spider', 'turkey',
    'turtle',
]


class SlowCompleter(Completer):
    """
    This is a completer that's very slow.
    """
    def __init__(self):
        self.loading = False

    def get_completions(self, document, complete_event):
        # TODO: checking this flag is not reliable, multiple instances of this
        #       generator could be running at the same time. Use something like
        #       `get_app().current_buffer.is_completing` in the future.
        self.loading = True
        word_before_cursor = document.get_word_before_cursor()

        try:
            for word in WORDS:
                if word.startswith(word_before_cursor):
                    time.sleep(.2)  # Simulate slowness.
                    yield Completion(word, -len(word_before_cursor))

        finally:
            # We use try/finally because this generator can be closed if the
            # input text changes before all completions are generated.
            self.loading = False


def main():
    # We wrap it in a ThreadedCompleter, to make sure it runs in a different
    # thread. That way, we don't block the UI while running the completions.
    slow_completer = SlowCompleter()

    # Add a bottom toolbar that display when completions are loading.
    def bottom_toolbar():
        return ' Loading completions... ' if slow_completer.loading else ''

    # Display prompt.
    text = prompt('Give some animals: ', completer=slow_completer,
                  complete_in_thread=True, complete_while_typing=True,
                  bottom_toolbar=bottom_toolbar,
                  complete_style=CompleteStyle.MULTI_COLUMN)
    print('You said: %s' % text)


if __name__ == '__main__':
    main()
