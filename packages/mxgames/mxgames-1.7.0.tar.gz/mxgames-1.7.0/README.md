[mxgames](https://github.com/MemoryD/mxgames) 是一个由 python 写的小游戏集合，基于 pygame。

### 安装

```shell
$ pip install mxgames
```



### 运行

以下命令可以获得一个游戏列表：

```shell
$ python -m mxgames
```

以下命令开始一个游戏：

```shell
$ python -m mxgames.gamename
```

`gamename` 是游戏名。



### 游戏介绍

- #### **life**

  经典的生命游戏，理论上不需要玩家操作，但是我增加了点击操作，增加更多的可能性和趣味性。

  ```shell
  $ python -m mxgames.life
  ```

  ![life](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/life.gif)

- #### **2048**

  移动方块，相同的方块会融合，一步步凑出 2048。大家应该也很熟悉。

  ```shell
  $ python -m mxgames.2048
  ```

  ![2048](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot//2048.gif)

- #### snake

  贪吃蛇，地球人都知道的游戏。

  ```shell
  $ python -m mxgames.snake
  ```

  ![snake](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/snake.gif)

- #### **AI snake**

  自动寻路的贪吃蛇，基于近似的哈密顿环，加入了一些优化，游戏无需操作，但是可以按空格键暂停，正常情况下都会吃满屏幕，但是效率不高，正在寻找更好的优化方法。

  ```shell
  $ python -m mxgames.ai_snake
  ```

  ![ai_snake](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/ai_snake.gif)

- #### **tetris**

  俄罗斯方块，也不用多说了.......因为偷懒就没有做一个小界面显示下一个方块，不过这样显得更有挑战性。

  ```shell
  python -m mxgames.tetris
  ```

  ![tetris](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/tetris.gif)

- #### **to_hell**

  完整名字是 To Hell with Johnny，国内一般翻译为 **是男人就下一百层**，左右两个方向键就能控制，挺有趣...

  ```shell
  python -m mxgames.to_hell
  ```

  ![to_hell](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/to_hell.gif)

- #### **Mine**

  扫雷，以前 Windows 上自带的游戏，也是一款生命力非常强的游戏，现在还有世界排名。我做的这个是 20 * 20 大小，66 个地雷，大概就是比中等难度难一点。操作方式没有变，可以左右键一起按。剩余地雷数和所用时间显示在标题栏。

  ```shell
  python -m mxgames.mine
  ```

  ![mine](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/mine.gif)


- #### **Schulte**

  舒尔特方格，是一个简单的用来测试和训练注意力水平的方法，方法是按顺序点击数字，计算点完全部 25 个数字所需的时间。具体的可以去查资料。

  ```shell
  python -m mxgames.schulte
  ```

  ![schulte](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/schulte.gif)

- #### **Maze**

  迷宫，大小是 30 * 30，使用 Prim 算法生成，还算有一定难度。使用方向键控制。

  ```shell
  python -m mxgames.maze
  ```

  ![maze](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/maze.gif)



- #### **Gobang**

  五子棋，规则很简单，谁先达成五子连珠的就获胜。这是一个双人游戏（因为不会写AI），黑为先手，这里没有加入更多复杂的先后手规则。

  ```shell
  python -m mxgames.gobang
  ```

  ![gobang](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/gobang.gif)

- #### **Sudoku**

  数独，就算没玩过也听过吧........最后要保证每行，每列，每个 3*3 的格子里都没有重复的数字，并且填满所有格子。算法保证每题都一定有解，但不一定是唯一解（太麻烦了，我们又不是用来比赛，随便一点）。

  因为时间太长，所以把动态图的重复帧删掉了，所以才会是这样子的效果。

  ```shell
  python -m mxgames.sudoku
  ```

  ![sudoku](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/sudoku.gif)

  