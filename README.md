# gzb_maze_gen
A maze map generator for Gazebo

```
usage: map_gen.py -s 15,15 -o 0,0 -l 1 -f maze -v
       For negative origin use '=' sign
       map_gen.py -s 5,5 -o=-5,-5 -l 2 -f maze -v

Creates an SDF file for Gazebo which contains a perfect maze

optional arguments:
  -h, --help      show this help message and exit
  -s , --size     specifies size of maze as MxN. By default <15,15>
  -o , --origin   position of top left corner on gazebo world. By default <0,0>
  -l , --length   length of square cell edges. By default <1>
  -f , --file     specifies the name of created SDF file. By default <maze>
  -v, --vector    enables creating vector drawing of maze with the same name of SDF file

Enjoy your map!
```

![alt text](https://i.imgur.com/jYac089.png "Example Map")
