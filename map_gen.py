import argparse
from maze_gen import Maze


class Map():
    def __init__(self, size, origin, length, name, vector) -> None:
        self.map = None

        size = size.split(",")
        self.nx = int(size[0])
        self.ny = int(size[1])

        origin = origin.split(",")
        self.ox = int(origin[0])
        self.oy = int(origin[1])

        self.length = length

        self.f_name = name

        self.v = vector

    def create_map(self):
        self.map = self.start_map()
        self.map += self.create_ground()
        self.map += self.start_maze()

        ix, iy = 0, 0
        maze = Maze(self.nx, self.ny, ix, iy)
        maze.make_maze()
        for y in range(self.ny):
            for x in range(self.nx):
                if maze.maze_map[x][y].walls['N']:
                    self.map += self.create_wall(x, y, 'h', self.ox, self.oy, self.length)
                if maze.maze_map[x][y].walls['W']:
                    self.map += self.create_wall(x, y, 'v', self.ox, self.oy, self.length)
                self.map += self.create_joint(x, y, self.ox, self.oy, self.length)
                if y == self.ny-1:
                    if maze.maze_map[x][y].walls['S']:
                        self.map += self.create_wall(x, y+1, 'h', self.ox, self.oy, self.length)
                    self.map += self.create_joint(x, y+1, self.ox, self.oy, self.length)
                if x == self.nx-1:
                    if maze.maze_map[x][y].walls['E']:
                        self.map += self.create_wall(x+1, y, 'v', self.ox, self.oy, self.length)
                    self.map += self.create_joint(x+1, y, self.ox, self.oy, self.length)
        self.map += self.create_joint(x+1, y+1, self.ox, self.oy, self.length)

        
        self.map += self.end_maze()
        self.map += self.end_map()
        if self.v:
            maze.write_svg(self.f_name+".svg")
        return self.map

    def start_map(self):
        return '<sdf version="1.4">\n  <world name="maze_world">\n'

    def end_map(self):
        return '  </world>\n</sdf>'

    def create_ground(self):
        return '''    <model name="ground">
      <static>true</static>
      <link name="ground_link">
        <collision name="collision1">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
            </plane>
          </geometry>
        </collision>
        <visual name="visual1">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
        </visual>
      </link>
    </model>
'''

    def start_maze(self):
        pass
        return '''		<model name='Untitled'>
	  <pose>0 0 0 0 -0 0</pose>
        '''
    
    def end_maze(self):
        return '''		  <static>1</static>
		</model>
        
        '''

    def create_wall(self, x, y, orientation, ox=0, oy=0, size = 1):
        if orientation == "h":
            ori = 0
            # x_ = x+0.5 + ox
            x_ = x*size+size/2.0 + ox
            y_ = -(y*size + oy)
        elif orientation == "v":
            ori = 1.5708 # 1.5708 rad 90deg
            x_ = x*size+ox
            # y_ = -(y+0.5+oy)
            y_ = -(y*size+size/2.0+oy)
        return f'''		  <link name='Wall_{x}_{y}_{orientation}'>
		    <collision name='Wall_0_Collision'>
		      <geometry>
		        <box>
		          <size>{size-0.1} 0.1 1.5</size>
		        </box>
		      </geometry>
		      <pose>0 0 0.75 0 -0 0</pose>
		    </collision>
		    <visual name='Wall_0_Visual'>
		      <pose>0 0 0.75 0 -0 0</pose>
		      <geometry>
		        <box>
		          <size>{size-0.1} 0.1 1.5</size>
		        </box>
		      </geometry>
		      <material>
		        <script>
		          <uri>file://media/materials/scripts/gazebo.material</uri>
		          <name>Gazebo/Grey</name>
		        </script>
		        <ambient>0.921569 0.807843 0.615686 1</ambient>
		      </material>
		      <meta>
		        <layer>0</layer>
		      </meta>
		    </visual>
		    <pose>{x_} {y_} 0 0 -0 {ori}</pose>
		  </link>
        '''

    def create_joint(self, x, y, ox=0, oy=0, size = 1):
        x = x*size+ox
        y = -(y*size+oy)
        return f'''	    <link name='Joint_{x}_{y}'>
		    <collision name='Wall_2_Collision'>
		      <geometry>
		        <box>
		          <size>0.1 0.1 1.5</size>
		        </box>
		      </geometry>
		      <pose>0 0 0.75 0 -0 0</pose>
		    </collision>
		    <visual name='Wall_2_Visual'>
		      <pose>0 0 0.75 0 -0 0</pose>
		      <geometry>
		        <box>
		          <size>0.1 0.1 1.5</size>
		        </box>
		      </geometry>
		      <material>
		        <script>
		          <uri>file://media/materials/scripts/gazebo.material</uri>
		          <name>Gazebo/Grey</name>
		        </script>
		        <ambient>0.721569 0.907843 0.215686 1</ambient>
		      </material>
		      <meta>
		        <layer>0</layer>
		      </meta>
		    </visual>
		    <pose>{x} {y} 0 0 -0 0</pose>
		  </link>
        '''

    def create_file(self):
        with open(self.f_name+".world", "w") as f:
            f.write(self.create_map())

    

def main():
    parser = argparse.ArgumentParser(
    description='Creates an SDF file for Gazebo which contains a perfect maze', epilog="Enjoy your map!",
    usage="map_gen.py -s 15,15 -o 0,0 -l 1 -f maze -v\n"
    "       For negative origin use '=' sign\n"
    "       map_gen.py -s 5,5 -o=-5,-5 -l 2 -f maze -v")

    parser.add_argument("-s", "--size", metavar="",type=str , default="15,15", help="specifies size of maze as MxN. By default <15,15>")
    parser.add_argument("-o", "--origin", metavar="",type=str , default="0,0", help="position of top left corner on gazebo world. By default <0,0>")
    parser.add_argument("-l", "--length", metavar="",type=int , default=1, help="length of square cell edges. By default <1>")
    parser.add_argument("-f", "--file", metavar="",type=str , default="maze", help="specifies the name of created SDF file. By default <maze>")
    parser.add_argument("-v", "--vector",action="store_true", help="enables creating vector drawing of maze with the same name of SDF file")
    args = parser.parse_args()

    map = Map(size=args.size, origin=args.origin, length=args.length, name=args.file, vector=args.vector)
    map.create_file()

if __name__=="__main__":
    main()

