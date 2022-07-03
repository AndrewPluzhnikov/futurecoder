# flake8: NOQA E501
import ast
import random
from textwrap import dedent
from typing import List

from core.exercises import generate_list, generate_string
from core.text import (
    ExerciseStep,
    MessageStep,
    Page,
    Step,
    VerbatimStep,
    search_ast,
    Disallowed,
)


class IntroducingDictionaries(Page):
    class first_dict(VerbatimStep):
        """
We've seen several types: `str`, `int`, `float`, `bool`, and `list`.
Only one of these types can contain multiple values: `list`.
Now we're going to learn about another container type: `dict`, short for ***dictionary***.

Think of the familiar kind of dictionary where you look up a word to find its definition or a translation in another language.
Dictionaries in Python are similar, but more general. You look up a *key* (e.g. a word) to get the associated *value* (e.g. a definition or translation).

For example, here's a little dictionary translating English words to French:
Run the line below in the shell.

    __program_indented__
        """
        
        def program(self):
            french = {'apple':'pomme', 'box': 'boite'}

    class dict_access(VerbatimStep):
        """
`french` is a dictionary with two key-value pairs:

- `'apple': 'pomme'` where `'apple'` is the key and `'pomme'` is the value.
- `'box': 'boite'` where `'box'` is the key and `'boite'` is the value.

Like lists, a comma (`,`) is used to separate items (key-value pairs) from each other. A colon (`:`) separates the keys from the values.
Note that curly brackets (`{}`) are used to create the dictionary instead of the square brackets (`[]`) used when writing lists.

Remember that with lists, you get values based on their *index*, i.e. their position in the list.
So if `words = ['apple', 'box']`, then `words[0]` is `'apple'` and `words[1]` is `'box'`.
Try this in the shell:

__program_indented__
        """

        auto_translate_program = False

        program = "french[0]"

        def check(self):
            return "KeyError" in self.result


    final_text = """
TODO"""
