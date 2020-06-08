# Ron Graham's Game

Ron Graham's Game is a numerical variant of Naughts and Crosses/ Tic-Tac-Toe. In the general form, the board is a square matrix of length `L >= 3`, Player 1 has stones for all the Odd numbers in the range `1:L`, Player 2 has stones for all the Even numbers in the range `2:(L-1)`, a player wins if it completes a row/column/diagonal and the sum equals `(1:L)L/2`.

Ron Graham's Game is the variant where `L==3`, it has shown that Ron Graham's Game has an optimal strategy for the Player 1 (Odds), the variant where `L=4` has been shown to have an optimal strategy for Player 2 (Evens).


## Usage

The file [RonGrahamsGame.py](RonGrahamsGame.py) is a self contained Python 3 file including the game and the optimiser to play against, it can be executed using:

    python ./RonGrahamsGame.py

It will first prompt you if you wish to level up (play against the optimiser), you can chose to do so, simply by pressing `Enter` (since it is the default option).

