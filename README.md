Souper
======

Prototype to cheat program for word soup game.

Souper creates a random letter grid, similar to those used in the quiz machine game "Word Soup"
(previously known as Word Up) and searches the board for the highest scoring words.
It then rearranges the board and finds the next highest word.

In addition to finding the highest scoring words, it evaluates the different possible resulting boards
and chooses an option that will remove awkward letters (such as Qs and Zs), mantain an optimum
vowel/constant ratio, attempt to match letters together intelligntly, keep the board roughly square so that
there is less chance of an insolvable tail and examine different endgames, in an attempt to clear the board.

Although the program consistently scores very high it still requires some improvements.
The square stage is not effectively linked with the endgame so that board clearances are not usual.
For it be useful the solving part of the program would have to be linked with a camera phone, 
that used OCR to read a board off a screen.