import operator

class Robot:
    """This class will be used to perform operations as part of the Ricochet Robot game traversal."""

    def __init__(self, row_count, column_count, start_coordinates, goal_coordinates, block_locations):
        self.row_count = row_count
        self.column_count = column_count
        self.start_node = Node(start_coordinates, current_heuristic = (abs(goal_coordinates[0] - start_coordinates[0]) + abs(goal_coordinates[1] - start_coordinates[1])), goal_coordinates = goal_coordinates, traversed_list = [start_coordinates])
        self.goal_coordinates = goal_coordinates
        self.block_locations = block_locations
        self.goal_found = False
        self.loop_exists = False
        self.visited_dict = {}
        self.visited_dict[start_coordinates] = self.start_node
        self.cost_dict = {}
        self.cost_dict[start_coordinates] = self.start_node.net_heuristic 
    
    def navigate_best_heuristic(self):
        """Function to iteratively traverse in all 4 directions and then select min net_heuristic_cost node for expansion."""
        navigation_node = self.start_node
        while navigation_node.coordinates != self.goal_coordinates:
            navigation_node.visited = True
            del self.cost_dict[navigation_node.coordinates]
            self.traverse(navigation_node, 'left')
            self.traverse(navigation_node, 'right')
            self.traverse(navigation_node, 'up')
            self.traverse(navigation_node, 'down')
            
            if self.cost_dict:
                sorted_cost_list = sorted(self.cost_dict.items(), key=operator.itemgetter(1))  
                navigation_node = self.visited_dict[sorted_cost_list[0][0]]    
            if not self.cost_dict or navigation_node.visited:
                self.loop_exists = True
                return
        self.goal_found = True
        return navigation_node
        
    def manhattan_distance(self, source, destination):
        """Calculates the manhattan distance between the given source and destination coordinate tuples"""
        return abs(destination[0] - source[0]) + abs(destination[1] - source[1])
    
    def traverse(self, node, direction):
        """While not encountered a block node/beyond edge of box or goal node, traverse along the same direction."""     
        [x,y] = self.direction_coordinates(direction)
        goal_found = False
        new_coordinates = node.coordinates
        while (self.is_valid((new_coordinates[0]-x, new_coordinates[1]-y))):
            ##Add coordinates to set to remember the goal_path
            new_coordinates = (new_coordinates[0] - x, new_coordinates[1] - y)
            ##Check Goal State
            if new_coordinates == self.goal_coordinates:
                ##Store current coordinates in the goal path dict
                goal_found = True
                goal_cost = node.current_heuristic + self.manhattan_distance(node.coordinates, new_coordinates)
                traversed_list = list(node.traversed_node_list)
                traversed_list.append(new_coordinates)
                if not self.visited_dict.get(new_coordinates):
                    self.visited_dict[new_coordinates] = Node(new_coordinates, current_heuristic = goal_cost, goal_coordinates = self.goal_coordinates, is_goal_node = True, traversed_list = traversed_list)
                    self.cost_dict[new_coordinates] = self.visited_dict[new_coordinates].net_heuristic
                else:
                    goal_node = self.visited_dict[new_coordinates]
                    if goal_node.net_heuristic > goal_cost:
                        #mark visited_node as expired & replace Node object in dict
                        goal_node.expired = True
                        self.visited_dict[new_coordinates] = Node(new_cordinates, current_heuristic = goal_cost, goal_coordinates = self.goal_coordinates, is_goal_node = True, traversed_list = traversed_list)
                        self.cost_dict[new_coordinates] = self.visited_dict[new_coordinates].net_heuristic
                    else:
                        goal_node.is_goal_node = True
                break
        
        #If goal not found, & not the same coordinates, use new_coordinates to create node. Replace existing node ony if better net heuristic cost exists
        if (not goal_found) and (new_coordinates != node.coordinates):
            current_heuristic = node.current_heuristic + self.manhattan_distance(node.coordinates, new_coordinates)
            net_heuristic = current_heuristic + self.manhattan_distance(new_coordinates, self.goal_coordinates)
            traversed_list = list(node.traversed_node_list)
            traversed_list.append(new_coordinates)
            if not self.visited_dict.get(new_coordinates):
                self.visited_dict[new_coordinates] = Node(new_coordinates, current_heuristic = current_heuristic, goal_coordinates = self.goal_coordinates, traversed_list = traversed_list)
                self.cost_dict[new_coordinates] = self.visited_dict[new_coordinates].net_heuristic
            else:
                if self.visited_dict[new_coordinates].net_heuristic > net_heuristic:
                    self.visited_dict[new_coordinates].expired = True
                    self.visited_dict[new_coordinates] = Node(new_coordinates, current_heuristic = current_heuristic, goal_coordinates = self.goal_coordinates, traversed_list = traversed_list)
                    self.cost_dict[new_coordinates] = self.visited_dict[new_coordinates].net_heuristic
        
    
    def is_valid(self, coordinates):
        """Check if coordinates are among the block node coordinates or if the edge of the box has been breached."""
        if (coordinates[0] < 0) or (coordinates[0] >= self.row_count) or (coordinates[1] < 0) or (coordinates[1] >= self.column_count) or (coordinates in self.block_locations):
            return False
        return True
    
    def direction_coordinates(self, direction):
        """Return the tuple representing the coordinate offset required to travel in the given direction."""
        dir_offset = {
            'left' : (0, 1), 
            'right' : (0, -1), 
            'up' : (1, 0), 
            'down' : (-1, 0)
        }
        return dir_offset.get(direction)
        
class Node:
    """This class represents the data structure corresponding to each coordinate used for heuristic evaluation comparison during traversal and expansion."""
    
    def __init__(self, coordinates, current_heuristic, goal_coordinates, traversed_list, is_goal_node = False):
        self.coordinates = coordinates
        self.visited = False
        self.current_heuristic = current_heuristic   #Equivalent to g(n)
        self.net_heuristic = current_heuristic + (abs(goal_coordinates[0] - self.coordinates[0]) + abs(goal_coordinates[1] - self.coordinates[1]))  #Equivalent to f(n) = g(n) + h(n)
        self.traversed_node_list = traversed_list #Set of tuples traversed so far
        self.expired = False
        self.is_goal_node = is_goal_node