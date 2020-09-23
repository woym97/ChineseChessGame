# portfolio-project

This is a representation of chinese chess, also known as "Xiangqi". Specific rules for this game can be found via this wiki page: [the Wikipedia page](https://en.wikipedia.org/wiki/Xiangqi).  

This repository contains 2 files:
    - XiangqiGame.py contains the actual implementation of the game itself
    - XiangqiGame_TEST.py is a unit test file that contains game cases
        - The last unit test in this file is a winning game from the 2015 Xiangqi championships

Here's a very simple example of how the class could be used:
```
game = XiangqiGame()
move_result = game.make_move('c1', 'e3')
black_in_check = game.is_in_check('black')
game.make_move('e7', 'e6')
state = game.get_game_state()
```
