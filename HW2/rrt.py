"""
Rapidly Exploring Random Tree (RRT) Path Planning Implementation

This module implements the RRT algorithm for path planning, which works by:
1. Incrementally building a tree by sampling random points
2. Connecting new points to the nearest node in the tree
3. Checking for collisions and maintaining feasible paths

ROBO 5000 HW2: Path Planning

Instructions:
------------
1. Add your name below
2. Complete all sections marked with "Student Task:" comments/docstrings
3. The main algorithm steps are in the `planning` and `steer` methods
4. Test your implementation with different obstacle configurations

Full Name: JEFFREY MITCHELL
"""

import math
import random
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

show_animation = True


class RRT:
    """RRT path planning implementation."""

    class Node:
        """A node in the RRT tree."""

        def __init__(self, x: float, y: float, yaw: float = 0.0):
            """
            Initialize a node.

            Args:
                x: X coordinate
                y: Y coordinate
            """
            self.x: float = x
            self.y: float = y
            self.path_x: List[float] = []
            self.path_y: List[float] = []
            self.parent: Optional["RRT.Node"] = None

    class AreaBounds:
        """Bounds for the planning area."""

        def __init__(self, area: List[float]):
            """
            Initialize area bounds.

            Args:
                area: List of [xmin, xmax, ymin, ymax]
            """
            self.xmin: float = float(area[0])
            self.xmax: float = float(area[1])
            self.ymin: float = float(area[2])
            self.ymax: float = float(area[3])

    def __init__(
        self,
        start: List[float],
        goal: List[float],
        obstacle_list: List[Tuple[float, float, float]],
        rand_area: List[float],
        expand_dis: float = 3.0,
        path_resolution: float = 0.5,
        goal_sample_rate: int = 5,
        max_iter: int = 500,
        play_area: Optional[List[float]] = None,
        robot_radius: float = 0.0,
    ):
        """
        Initialize the RRT planner.

        Args:
            start: Start position [x, y]
            goal: Goal position [x, y]
            obstacle_list: List of obstacles [(x, y, radius), ...]
            rand_area: Random sampling area [min, max]
            expand_dis: Maximum distance to expand tree
            path_resolution: Resolution for path checking
            goal_sample_rate: Rate at which goal is sampled instead of random point
            max_iter: Maximum number of iterations
            play_area: Optional bounds for valid area [xmin, xmax, ymin, ymax]
            robot_radius: Radius of robot for collision checking

        Class Attributes:
            self.start: Node object representing start position
            self.end: Node object representing goal position
            self.min_rand: Minimum value for random sampling range
            self.max_rand: Maximum value for random sampling range
            self.play_area: AreaBounds object defining valid planning space (None if unbounded)
            self.expand_dis: Maximum distance to extend tree in each iteration
            self.path_resolution: Distance between intermediate points when extending tree
            self.goal_sample_rate: Probability (in %) of sampling goal instead of random point
            self.max_iter: Maximum number of iterations for tree expansion
            self.obstacle_list: List of obstacles, each defined by (x, y, radius)
            self.node_list: List of all nodes in the tree
            self.robot_radius: Robot's physical size for collision checking
        """
        # Create Node objects for start and goal positions
        self.start: "RRT.Node" = self.Node(start[0], start[1])
        self.end: "RRT.Node" = self.Node(goal[0], goal[1])
        # Random sampling bounds
        self.min_rand: float = rand_area[0]
        self.max_rand: float = rand_area[1]
        # Create AreaBounds object if play_area is specified
        self.play_area: Optional["RRT.AreaBounds"]
        if play_area is not None:
            self.play_area = self.AreaBounds(play_area)
        else:
            self.play_area = None
        # Tree expansion parameters
        self.expand_dis: float = expand_dis
        self.path_resolution: float = path_resolution
        self.goal_sample_rate: int = goal_sample_rate
        self.max_iter: int = max_iter
        # Environment and planning data
        self.obstacle_list: List[Tuple[float, float, float]] = obstacle_list
        self.node_list: List["RRT.Node"] = []
        self.robot_radius: float = robot_radius

    def get_random_node(self) -> "RRT.Node":
        """
        Sample a random node in the state space.

        The sampling should account for:
        - goal_sample_rate: Probability of sampling the goal node
        - min_rand/max_rand: Bounds of the sampling space

        Student Task:
        ------------
        1. With probability goal_sample_rate/100, return the goal node
        2. Otherwise, sample random position within min_rand/max_rand bounds
        4. Return new Node with sampled values

        Returns:
            Node: Randomly sampled node
        """
        # YOUR CODE GOES HERE
        # Use goal_sample_rate to bias sampling towards goal
        # Sample random position within bounds
        
        
        if random.randint(0, 100) < self.goal_sample_rate:
            # goal sample
            return self.Node(self.end.x, self.end.y)
        else:
            # random sample
            x = random.uniform(self.min_rand, self.max_rand)
            y = random.uniform(self.min_rand, self.max_rand)
            
            return RRT.Node(x,y)

    def calc_dist_to_goal(self, x: float, y: float) -> float:
        """Calculate distance from current position to the goal."""
        dx = x - self.end.x
        dy = y - self.end.y
        return math.hypot(dx, dy)

    def generate_final_course(self, goal_ind: int) -> List[Tuple[float, float]]:
        """Generate the final path from the goal node to the start node.

        Args:
            goal_ind: Index of the goal node in node_list

        Returns:
            path: List of points along the path
        """
        path: List[Tuple[float, float]] = []
        node = self.node_list[goal_ind]

        # For standard RRT, just use node positions
        while node.parent is not None:
            path.append((node.x, node.y))
            node = node.parent
        path.append((node.x, node.y))

        return path[::-1]  # Reverse path to get start-to-goal order

    def planning(
        self, animation: bool = True
    ) -> Optional[List[Tuple[float, float]]]:
        """
        Plan a path from start to goal using RRT.

        Args:
            animation: Whether to show animation of tree growth

        Returns:
            path: List of points [(x1,y1), (x2,y2),...] or None if no path found

        Student Task:
        ------------
        1. Initialize the tree with the start node (add to node_list)
        2. For max_iter iterations:
           a. Sample random point using get_random_node()
           b. Find nearest node in tree
           c. Attempt to steer towards sampled point
           d. If valid new node:
              - Add to tree
              - Check if goal is reachable
              - If goal reached, extract and return path
        3. Return None if no path found
        """
        self.node_list = [self.start]

        rnd_node: Optional["RRT.Node"] = None
        for i in range(self.max_iter):
            # YOUR CODE GOES HERE
            # Use get_random_node() to sample a random configuration
            # Find nearest node in the tree
            # Steer towards the sampled node
            # Check for collisions and validity
            
            rnd_node = self.get_random_node()
            nearest_node = self.find_nearest_node(rnd_node)
            steered_node = self.steer(nearest_node, rnd_node, self.expand_dis)
            
            collision_free = self.check_collision(steered_node, self.obstacle_list)
            if collision_free: self.node_list.append(steered_node)

            # DO NOT ALTER THE NEXT 2 LINES
            if animation and i % 5 == 0:
                self.draw_graph(rnd_node)

            # YOUR CODE GOES HERE
            # Check if goal is reachable from new node
            # from current node connect to goal node and find the path - return path after plotting path (below)
            path: Optional[List[Tuple[float, float]]] = None
            if not collision_free: continue
            if not self.calc_dist_to_goal(steered_node.x, steered_node.y) <= self.expand_dis: continue
            
            final_node_candidate = self.steer(steered_node, self.end, self.expand_dis)
                
            if not self.check_collision(final_node_candidate, self.obstacle_list): continue
            
            self.node_list.append(final_node_candidate)
            path = self.generate_final_course(len(self.node_list) - 1)
            
            if path is not None:
                if animation:
                    # For standard RRT, plot straight lines
                    path_x = [x for (x, y) in path]
                    path_y = [y for (x, y) in path]
                    plt.plot(
                        path_x,
                        path_y,
                        "-r",
                        linewidth=2,
                        label="Final Path",
                    )
                    plt.legend()
                    plt.pause(0.01)
                return path

        return None

    def steer(
        self,
        from_node: "RRT.Node",
        to_node: "RRT.Node",
        extend_length: float = float("inf"),
    ) -> "RRT.Node":
        """
        Steer from one node towards another within constraints.

        Args:
            from_node: Node to steer from
            to_node: Node to steer towards
            extend_length: Maximum distance to extend

        Returns:
            new_node: New node after steering

        Student Task:
        ------------
        1. Create new node at from_node location
        2. Calculate distance and angle to to_node
        3. If distance > extend_length:
           - Scale movement to respect extend_length
        4. Move towards to_node:
           - Update position incrementally using path_resolution
           - Store path points in new_node.path_x and new_node.path_y
        5. Set parent relationship
        6. Return new node
        """
        new_node = self.Node(from_node.x, from_node.y)
        distance, theta = self.calc_distance_and_angle(
            new_node, to_node
        )  # This function returns the distance d from new_node to to_node and the theta represents the angle the line joining them makes with the x axis

        new_node.path_x = [new_node.x]
        new_node.path_y = [new_node.y]
        # YOUR CODE GOES HERE
        # If extend_length is greater than the distance, then ensure the robot doesn't go beyong extend_length
        # Propagate the robot iteratively from new_node to to_node until extend_length is reached
        # Use check_collision to check if the robot is colliding with an obstacle
        # If the robot is colliding with an obstacle, then stop the propagation
        # Append the coordinates of the robot into new_node.path_x and new_node.path_y

        # walk along path to new node
        extend_length = min(extend_length, distance)
        steps = math.floor(extend_length / self.path_resolution)
        for step in range(1, steps + 1):
            h = self.path_resolution * step
            new_node.path_x.append(from_node.x + math.cos(theta) * h)
            new_node.path_y.append(from_node.y + math.sin(theta) * h)

        new_node.x = new_node.path_x[-1]
        new_node.y = new_node.path_y[-1]

        
        d, _ = self.calc_distance_and_angle(
            new_node, to_node
        )  # We want to check if the robot has reached to_node
        # YOUR CODE GOES HERE
        # Check if the robot has reached to_node. If yes, add to_node coordinates to the path of new_node
        # Add from_node as parent of new_node
        
        # snap
        if d <= self.path_resolution:
            new_node.path_x.append(to_node.x)
            new_node.path_y.append(to_node.y)
            new_node.x = to_node.x
            new_node.y = to_node.y
            
        new_node.parent = from_node

        return new_node

    @staticmethod
    def calc_distance_and_angle(
        from_node: "RRT.Node", to_node: "RRT.Node"
    ) -> Tuple[float, float]:
        """
        Calculate distance and angle between nodes.

        Args:
            from_node: Starting node
            to_node: Target node

        Returns:
            distance: Euclidean distance between nodes
            theta: Angle in radians from from_node to to_node

        Student Task:
        ------------
        1. Calculate Euclidean distance between nodes
        2. Calculate angle of line from from_node to to_node
           relative to x-axis (use math.atan2)
        3. Return distance and angle
        """
        distance: float
        theta: float
        # YOUR CODE GOES HERE
        # Write code to find the distance between from_node and to_node
        # and the angle made by the line joining from_node and to_node with the x_axis
        
        distance = math.dist((from_node.x, from_node.y), (to_node.x, to_node.y))
        theta = math.atan2(to_node.y - from_node.y, to_node.x - from_node.x)
        
        return distance, theta

    def find_nearest_node(self, node: "RRT.Node") -> "RRT.Node":
        """
        Find the nearest node in the tree to the given node.

        Args:
            node: Node to find nearest node to

        Returns:
            nearest_node: Nearest node in the tree

        Student Task:
        ------------
        1. Initialize variables for tracking nearest node and minimum distance
        2. Iterate through node_list
        3. Calculate distance to each node
        4. Update nearest node if current distance is smaller
        5. Return the nearest node found
        """
        # nearest_node = None
        # min_distance: float = float("inf")
        # YOUR CODE HERE
        
        nearest_node = min(self.node_list, key=lambda candidate_node: math.dist((node.x, node.y), (candidate_node.x, candidate_node.y)))
        
        return nearest_node

    def check_collision(
        self, node: "RRT.Node", obstacle_list: List[Tuple[float, float, float]]
    ) -> bool:
        """
        Check if the node (and its path to parent) collides with any obstacles.

        Args:
            node: Node to check for collision
            obstacle_list: List of obstacles [(x, y, radius), ...]

        Returns:
            collision_free: True if node is collision-free, False otherwise

        Student Task:
        ------------
        1. For each obstacle:
           - Calculate distance from node to obstacle center
           - Check if distance is less than obstacle radius + robot_radius
        2. Return True if no collisions, False otherwise
        """
        # YOUR CODE GOES HERE
        for obstacle_x, obstacle_y, radius in obstacle_list:
            for path_x, path_y in zip(node.path_x, node.path_y):
                if math.dist((path_x, path_y), (obstacle_x, obstacle_y)) <= radius + self.robot_radius:
                    return False
                
        return True


    def draw_graph(self, rnd: Optional["RRT.Node"] = None) -> None:
        plt.clf()
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect(
            "key_release_event",
            lambda event: [exit(0) if event.key == "escape" else None],
        )
        if rnd is not None:
            plt.plot(rnd.x, rnd.y, "^k")
            if self.robot_radius > 0.0:
                self.plot_circle(rnd.x, rnd.y, self.robot_radius, "-r")
        for node in self.node_list:
            if node.parent:
                plt.plot(node.path_x, node.path_y, "-g")

        for ox, oy, size in self.obstacle_list:
            self.plot_circle(ox, oy, size)

        plt.plot(self.start.x, self.start.y, "xr")
        plt.plot(self.end.x, self.end.y, "xr")
        plt.axis("equal")
        plt.axis((self.min_rand, self.max_rand, self.min_rand, self.max_rand))
        plt.grid(True)
        plt.pause(0.01)

    @staticmethod
    def plot_circle(x: float, y: float, size: float, color: str = "-b") -> None:
        deg = list(range(0, 360, 5))
        deg.append(0)
        xl = [x + size * math.cos(np.deg2rad(d)) for d in deg]
        yl = [y + size * math.sin(np.deg2rad(d)) for d in deg]
        plt.plot(xl, yl, color)


def main(goal_x: float = 6.0, goal_y: float = 10.0) -> None:
    print("start " + __file__)
    obstacleList: List[Tuple[float, float, float]] = [
        (5, 5, 1),
        (3, 6, 2),
        (3, 8, 2),
        (3, 10, 2),
        (7, 5, 2),
        (9, 5, 2),
        (8, 10, 1),
    ]  # [x, y, radius]

    # Initialize plot
    plt.ion()  # Enable interactive mode
    plt.figure(figsize=(10, 10))

    rrt = RRT(
        start=[0, 0],
        goal=[goal_x, goal_y],
        rand_area=[-2, 15],
        obstacle_list=obstacleList,
        robot_radius=0.8,
    )

    # Run planning
    path = rrt.planning(animation=show_animation)

    if path is None:
        print("Cannot find path")
    else:
        print("found path!!")

    plt.ioff()  # Disable interactive mode
    plt.show()  # This will block until the window is closed


if __name__ == "__main__":
    main()  # Run standard RRT

"""
Qeustion 6 response:

Setting expand_dist to something tiny like 0.1 will fail in two ways:

Most critically, this places it beneath the stock path_resolution. steer takes floor(extend_length / path_resolution) increments.
This would work out to 0 under the above conditions path_resolution must be reduced below expand_dist.

That alone will likely not be enough. Our steps are now quite tiny, and we will need to massively
boost the max time steps to compensate, lest the simulation end before the goal is reached.

"""

