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

    class dict_access2(VerbatimStep):
        """
That doesn't work because the position of items in a dictionary usually doesn't matter.

You don't usually care what's the 2nd or 5th or 100th word of the dictionary,
you just want to find a specific word like 'apple'. So try that instead:

__program_indented__
        """

        auto_translate_program = False

        program = "french['apple']"

        def check(self):
            return "pomme" in self.result

    class dict_access3(VerbatimStep):
        """
That's better!

Now run a similar line in the shell to look up the translation for 'box'.

__program_indented__
        """
        ##TODO: Hide the program from the user but still let them proceed through the excercise
        auto_translate_program = False

        program = "french['box']"

        def check(self):
            return "boite" in self.result

    class dict_access4(VerbatimStep):
        """
And now you know both Python and French!

Now let's translate from French to English:

__program_indented__
        """

        auto_translate_program = False

        program = "french['pomme']"

        def check(self):
            return "KeyError" in self.result

    final_text = """
Sorry, you can't do that either. You can only look up a key to get its value, not the other way around.

The dictionary `french` only has 2 keys: `'apple'` and `'box'`. `'pomme'` is a value, not a key.

We'll soon learn why you can't just look up values directly, and what you can do about it.


Note that both `french[0]` and `french['pomme']` raised the same type of error: a `KeyError`.

This error means that the provided key (`0` or `'pomme'` in this case) wasn't found in the dictionary.

It's not that `french[0]` isn't *allowed*, it's just that it means the same thing as always:
find the value associated with the key `0`. In this case it finds that no such key exists.

But `0` *could* be a key, because many types of keys are allowed, including strings and numbers.
"""


class UsingDictionaries(Page):
    class shopping_cart1(VerbatimStep):
        """
Let's see dictionaries in a real life problem. Imagine you're building an online shopping website.

You keep the prices of all your items in a dictionary:

__program_indented__
        """

        auto_translate_program = False

        program = "prices = {'apple': 2, 'box': 5, 'cat': 100, 'dog': 100}"


    class shopping_cart2(VerbatimStep):
        """
Here you can see one reason why looking up values in a dictionary could be a problem.

What would `prices[100]` be? `'dog'`? `'cat'`? `['dog', 'cat']`?

The same value can be repeated any number of times in a dictionary.

On the other hand, keys have to be unique. Imagine if your prices started like this:

__program_indented__
        """

        auto_translate_program = False

        program = "prices = {'apple': 2, 'apple': 3}"


    class shopping_cart3(VerbatimStep):
        """
How much does an apple cost? We know it's `prices['apple']`, but is that `2` or `3`?

Clearly there should only be one price, so duplicate keys aren't allowed.


Anyway, this is a normal shop where things have one price.

This normal shop has normal customers with normal shopping lists like `['apple', 'box', 'cat']`.

And even though your customers have calculators in their pockets, they still expect you to add up all the prices
yourself and tell them how much this will all cost, because that's what normal shops do.

So let's write a function that does that. Complete the function below, particularly the line `price = ...`


    __copyable__
    __program_indented__
        """

        def program(self):
            def total_cost(cart, prices):
                result = 0
                for item in cart:
                    price = ... 
                    result += price
                return result

            assert_equal(
                total_cost(
                    ['apple', 'box', 'cat'],
                    {'apple': 2, 'box': 5, 'cat': 100, 'dog': 100},
                    ),
                107,
            )
        

    class shopping_cart4(VerbatimStep):
        """
Perfect! You publish your website and start dreaming about how rich you're going to be.

But soon you get a complaint from a customer who wants to buy 5 million dogs...and 2 boxes to put them in.

Your website allows buying the same items several times, e.g. `total_cost(['box', 'box'], {...})` works,
but they have to add each item one at a time, and for some reason this customer doesn't want to click
'Add to Cart' 5 million times. People are so lazy!

Here's the new code for you to fix:

    __copyable__
    __program_indented__
        """

        def program(self):
            def total_cost(cart, quantities, prices):
                result = 0
                for item in cart:
                    price = ...
                    quantity = ...
                    result += price * quantity
                return result

            assert_equal(
                total_cost(
                    ['dog', 'box'],
                    {'dog': 5000000, 'box': 2},
                    {'apple': 2, 'box': 5, 'cat': 100, 'dog': 100},
                ),
                500000010,
            )


    class shopping_cart5(VerbatimStep):
        """
We've added another parameter called `quantities` to `total_cost`.
Now `cart` is still a list of strings, but it doesn't have any duplicates.
`quantities` is a dictionary where the keys are the items in `cart` and the corresponding values are the quantity
of that item that the customer wants to buy.


Not bad! But you may have noticed that it looks a bit awkward. Why do we have to specify `'dog'` and `'box'` in both the `cart` and the `quantities`?

On the next page we'll look at how to loop directly over the keys of a dictionary,
so we can get rid of the `cart` argument.


But first, let's practice what we've learned a bit more.

[Earlier in the course](#IntroducingElif) we looked at converting one strand of DNA
into a new strand with matching nucleotides:

    __copyable__
    __program_indented__
        """

        def program(self):
            def substitute(string):
                result = ''
                for char in string:
                    if char == 'A':
                        char = 'T'
                    elif char == 'T':
                        char = 'A'
                    elif char == 'G':
                        char = 'C'
                    elif char == 'C':
                        char = 'G'
                    result += char
                return result

            original = 'AGTAGCGTCCTTAGTTACAGGATGGCTTAT'
            expected = 'TCATCGCAGGAATCAATGTCCTACCGAATA'
            assert_equal(substitute(original), expected)


    ##TODO: Is this supposed to be an exercise or a verbatim step?
    class dna_part2(VerbatimStep):
        """
Now we can use dictionaries to make this code both shorter and more general so it can be used for other purposes.

Your job is to add another argument to the `substitute` function: a dictionary called `d`.

The keys of `d` represent characters
in the first argument `string` that should be replaced by the corresponding values of `d`. For example, `'A': 'T'`
means that `A` should be replaced by `T`:

    __copyable__
    __program_indented__
        """
        
        def program(self):
            def substitute(string, d):
                ...

            original = 'AGTAGCGTCCTTAGTTACAGGATGGCTTAT'
            expected = 'TCATCGCAGGAATCAATGTCCTACCGAATA'
            assert_equal(substitute(original, {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}), expected)


    class cryptography(VerbatimStep):
        """
Nice! Here's an example of how this function can also be used to encrypt and decrypt secret messages:

    __copyable__
    __program_indented__
        """

        def program(self):
            plaintext = 'helloworld'
            encrypted = 'qpeefifmez'
            letters = {'h': 'q', 'e': 'p', 'l': 'e', 'o': 'f', 'w': 'i', 'r': 'm', 'd': 'z'}
            reverse = {'q': 'h', 'p': 'e', 'e': 'l', 'f': 'o', 'i': 'w', 'm': 'r', 'z': 'd'}
            assert_equal(substitute(plaintext, letters), encrypted)
            assert_equal(substitute(encrypted, reverse), plaintext)


    final_text = """
The same function works in both directions, we just need to pass it different dictionaries.

The two dictionaries are almost the same, we just swap around the key and value in each pair.
So to encrypt, we replace `e` with `p`, and to decrypt we change `p` back to `e`.

Note that `'e'` is both a key and a value in `letters`.

Looking up `letters['e']` means that we're asking about `'e'` as a *key*, so it gives `'p'`.
Remember, we can't use `letters` to ask which key is associated with `'e'` as a *value*.
But in this case we can use the other dictionary for that: `reverse['e']` gives `'l'`,
and `letters['l']` gives `'e'` again.

Soon you'll write a function to create a dictionary like `reverse` automatically,
i.e. `reverse = swap_keys_values(letters)`."""
