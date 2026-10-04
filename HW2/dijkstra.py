"""

Grid-based Dijkstra Path Planning Implementation

This module implements Dijkstra's algorithm for path planning on a 2D grid with obstacles.
The implementation allows for 8-directional movement (horizontal, vertical, and diagonal)
and handles obstacle avoidance.

ROBO 5000 HW2: Path Planning

Instructions:
------------
1. Add your name below
2. Complete all sections marked with "Student Task:" comments/docstrings
3. The main algorithm steps are in the `planning` method
4. Test your implementation with different obstacle configurations in main()

Full Name: ADD YOUR NAME HERE
"""

import math
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt

show_animation = True


class Dijkstra:
    """Dijkstra's algorithm implementation for grid-based path planning."""

    def __init__(
        self,
        obstacle_x: List[float],
        obstacle_y: List[float],
        resolution: float,
        robot_radius: float,
    ):
        """
        Initialize the Dijkstra path planner.

        Args:
            obstacle_x: List of x coordinates of obstacles
            obstacle_y: List of y coordinates of obstacles
            resolution: Grid resolution (cell size)
            robot_radius: Radius of the robot for collision checking

        Class Attributes:
            self.min_x: Minimum x-coordinate of the grid world boundary
            self.min_y: Minimum y-coordinate of the grid world boundary
            self.max_x: Maximum x-coordinate of the grid world boundary
            self.max_y: Maximum y-coordinate of the grid world boundary
            self.x_width: Number of grid cells along x-axis
            self.y_width: Number of grid cells along y-axis
            self.obstacle_map: 2D boolean array marking obstacle positions (True = obstacle present)
            self.resolution: Size of each grid cell (determines grid granularity)
            self.robot_radius: Robot's physical size for collision checking
            self.motion: List of possible movement directions and their costs
        """
        # Grid world boundaries (initialized in calc_obstacle_map)
        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None
        # Grid dimensions in number of cells (initialized in calc_obstacle_map)
        self.x_width = None
        self.y_width = None
        # 2D array marking obstacle locations (initialized in calc_obstacle_map)
        self.obstacle_map = None

        # Grid cell size
        self.resolution = resolution
        # Robot's physical size for collision checking
        self.robot_radius = robot_radius
        # Create obstacle map from given coordinates
        self.calc_obstacle_map(obstacle_x, obstacle_y)
        # Get possible movement directions and their costs
        self.motion = self.get_motion_model()

    class Node:
        """A node in the Dijkstra search grid."""

        def __init__(self, x: int, y: int, cost: float, parent_index: int):
            """
            Initialize a search node.

            Args:
                x: Grid x coordinate
                y: Grid y coordinate
                cost: Cost to reach this node from start
                parent_index: Index of parent node in the closed set
            """
            self.x = x  # index of grid
            self.y = y  # index of grid
            self.cost = cost
            self.parent_index = parent_index  # index of previous Node

    def planning(
        self, start_x: float, start_y: float, goal_x: float, goal_y: float
    ) -> Tuple[List[float], List[float]]:
        """
        Plan a path from start to goal position using Dijkstra's algorithm.

        Args:
            start_x: Start x coordinate
            start_y: Start y coordinate
            goal_x: Goal x coordinate
            goal_y: Goal y coordinate

        Returns:
            rx, ry: Lists of x and y coordinates of the path from goal to start

        -------------------------------------------------------
        Student Task: Complete Dijkstra's algorithm implementation:
        1. Initialize start and goal nodes (already done for you)
        2. While open_set is not empty:
           a. Find node with minimum cost in open_set (use node.cost)
           b. If node is goal, update goal_node and break
           c. Remove current node from open_set and add to closed_set
           d. For each possible motion in self.motion:
              - Calculate new node position and cost
              - Skip if in closed_set or out of bounds
              - Add to open_set if new, or update if found better path

        Key Differences from A*:
        - No heuristic function needed
        - Simply use the cost from start (g-cost) to determine next node
        - Expands in all directions equally until goal is found
        """
        start_node = self.Node(
            self.calc_xy_index(start_x, self.min_x),
            self.calc_xy_index(start_y, self.min_y),
            0.0,
            -1,
        )
        goal_node = self.Node(
            self.calc_xy_index(goal_x, self.min_x),
            self.calc_xy_index(goal_y, self.min_y),
            0.0,
            -1,
        )

        open_set, closed_set = dict(), dict()
        open_set[self.calc_grid_index(start_node)] = start_node

        while True:
            # YOUR CODE GOES HERE
            # Find the Node in open_set with least cost and assign it to current
            current = None  # Replace None with code to assign the least costly node in open_set

            # DO NOT ALTER THE NEXT 8 LINES.
            if show_animation:  # pragma: no cover
                plt.plot(
                    self.calc_grid_position(current.x, self.min_x),
                    self.calc_grid_position(current.y, self.min_y),
                    "xc",
                )
                plt.gcf().canvas.mpl_connect(
                    "key_release_event",
                    lambda event: [exit(0) if event.key == "escape" else None],
                )
                if len(closed_set.keys()) % 10 == 0:
                    plt.pause(0.001)

            # YOUR CODE GOES HERE
            # 1. Check if current node is goal node:
            #    - If yes: Update goal_node.parent_index and cost, then break

            # 2. Move current node from open_set to closed_set

            # 3. Expand neighbors using motion model:
            #    - Skip if in closed_set
            #    - Skip if out of bounds
            #    - Add to open_set if new
            #    - Update if better path found

        rx, ry = self.calc_final_path(goal_node, closed_set)
        return rx, ry

    def calc_final_path(
        self, goal_node: Node, closed_set: Dict[int, Node]
    ) -> Tuple[List[float], List[float]]:
        """
        Calculate the final path from start to goal node.

        Args:
            goal_node: The goal node
            closed_set: Set of expanded nodes

        Returns:
            rx, ry: Lists of x and y coordinates of the path
        """
        rx, ry = [self.calc_grid_position(goal_node.x, self.min_x)], [
            self.calc_grid_position(goal_node.y, self.min_y)
        ]
        parent_index = goal_node.parent_index
        while parent_index != -1:
            n = closed_set[parent_index]
            rx.append(self.calc_grid_position(n.x, self.min_x))
            ry.append(self.calc_grid_position(n.y, self.min_y))
            parent_index = n.parent_index

        return rx, ry

    def calc_grid_position(self, index: int, min_position: float) -> float:
        """
        Calculate grid position from index.

        Args:
            index: Grid index
            min_position: Minimum position value

        Returns:
            Actual position coordinate
        """
        pos = index * self.resolution + min_position
        return pos

    def calc_xy_index(self, position: float, min_position: float) -> int:
        """
        Calculate grid index from position.

        Args:
            position: Actual position coordinate
            min_position: Minimum position value

        Returns:
            Grid index
        """
        return round((position - min_position) / self.resolution)

    def calc_grid_index(self, node: Node) -> int:
        """
        Calculate unique index for grid position.

        Args:
            node: Node to calculate index for

        Returns:
            Unique grid index
        """
        return node.y * self.x_width + node.x

    def verify_node(self, node: Node) -> bool:
        """
        Verify if a node is valid for path planning.

        This function checks two conditions:
        1. If the node's coordinates are within the grid boundaries
        2. If the node's position doesn't collide with any obstacles

        Args:
            node: The node to verify, containing x and y coordinates in grid units

        Returns:
            bool: True if the node is valid (within bounds and collision-free),
                 False otherwise

        Student Task:
        ------------
        1. Check if node coordinates (node.x, node.y) are within grid bounds:
           - x should be between 0 and self.x_width
           - y should be between 0 and self.y_width
        2. If within bounds, check self.obstacle_map to see if the node
           position collides with an obstacle
        3. Return False if either check fails, True if both pass
        """
        # YOUR CODE GOES HERE
        # Verify if the node is within bounds and isn't colliding with an obstacle
        # Return False if node is invalid. Otherwise, return True
        pass  # REMOVE THIS LINE WHEN DONE

    def calc_obstacle_map(
        self, obstacle_x: List[float], obstacle_y: List[float]
    ) -> None:
        """
        Calculate a grid-based obstacle map from obstacle coordinates.

        This function converts continuous obstacle coordinates into a discrete grid
        representation where each cell is marked as either containing an obstacle or not.

        Args:
            obstacle_x: List of x-coordinates of obstacles in world units
            obstacle_y: List of y-coordinates of obstacles in world units

        Note:
            - The function updates these class attributes:
              * self.min_x, self.min_y: Minimum x,y coordinates of the grid
              * self.max_x, self.max_y: Maximum x,y coordinates of the grid
              * self.x_width, self.y_width: Width and height of the grid
              * self.obstacle_map: 2D grid marking obstacle positions

        Student Task:
        ------------
        1. Find grid boundaries:
           - Calculate min/max x,y from obstacle coordinates
           - Convert to grid coordinates using self.resolution
           - Store in self.min_x, self.min_y, self.max_x, self.max_y

        2. Calculate grid dimensions:
           - Use min/max values to compute grid width and height
           - Store in self.x_width and self.y_width

        3. After the obstacle_map is initialized (DO NOT MODIFY THE INITIALIZATION):
           - Convert each obstacle coordinate to grid coordinates to find the nearest cell
           - Find the absolute x,y coords of the nearest cell
           - If the robot was placed at the x,y coords above, would it collide with the obstacle point, given the robot radius
           - Mark corresponding cells in obstacle_map as True
        """
        # YOUR CODE GOES HERE
        # Find the minimum and maximum bounds for x and y
        # Use the bounds to obtain the width along x and y axes and store them in self.x_width and self.y_width respectively

        # DO NOT ALTER THE NEXT TWO LINES.
        self.obstacle_map = [
            [False for _ in range(self.y_width)] for _ in range(self.x_width)
        ]

        # For each cell in self.obstacle_map, use the calculations above to assign it as
        # boolean True if the cell overlaps with an obstacle and boolean False if it doesn't
        pass  # REMOVE THIS LINE WHEN DONE

    @staticmethod
    def get_motion_model() -> List[List[float]]:
        """
        Define the possible movement directions and their costs.

        Returns:
            List of [dx, dy, cost] for each possible movement
        """
        # dx, dy, cost
        motion = [
            [1, 0, 1],
            [0, 1, 1],
            [-1, 0, 1],
            [0, -1, 1],
            [-1, -1, math.sqrt(2)],
            [-1, 1, math.sqrt(2)],
            [1, -1, math.sqrt(2)],
            [1, 1, math.sqrt(2)],
        ]
        return motion


def main():
    print(__file__ + " start!!")

    # start and goal position
    start_x = 5.0  # [m]
    start_y = 5.0  # [m]
    goal_x = 50.0  # [m]
    goal_y = 50.0  # [m]
    cell_size = 2.0  # [m]
    robot_radius = 1.0  # [m]

    # Feel free to change the obstacle positions and test the implementation on various scenarios
    obstacle_x, obstacle_y = [], []
    for i in range(0, 60):
        obstacle_x.append(i)
        obstacle_y.append(0.0)
    for i in range(0, 60):
        obstacle_x.append(60.0)
        obstacle_y.append(i)
    for i in range(0, 61):
        obstacle_x.append(i)
        obstacle_y.append(60.0)
    for i in range(0, 61):
        obstacle_x.append(0.0)
        obstacle_y.append(i)
    for i in range(0, 40):
        obstacle_x.append(20.0)
        obstacle_y.append(i)
    for i in range(0, 40):
        obstacle_x.append(40.0)
        obstacle_y.append(60.0 - i)

    if show_animation:
        plt.plot(obstacle_x, obstacle_y, ".k")
        plt.plot(start_x, start_y, "og")
        plt.plot(goal_x, goal_y, "xb")
        plt.grid(True)
        plt.axis("equal")

    dijkstra = Dijkstra(obstacle_x, obstacle_y, cell_size, robot_radius)
    rx, ry = dijkstra.planning(start_x, start_y, goal_x, goal_y)

    if show_animation:
        plt.plot(rx, ry, "-r")
        plt.pause(0.01)
        plt.show()


if __name__ == "__main__":
    main()
