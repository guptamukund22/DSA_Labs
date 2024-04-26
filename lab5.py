class MetroStop:
    def __init__(self, name, metro_line, fare):
        self.stop_name = name
        self.next_stop = None
        self.prev_stop = None
        self.line = metro_line
        self.fare = fare

    def get_stop_name(self):
        return self.stop_name

    def get_next_stop(self):
        return self.next_stop

    def get_prev_stop(self):
        return self.prev_stop

    def get_line(self):
        return self.line

    def get_fare(self):
        return self.fare

    def set_next_stop(self, next_stop):
        self.next_stop = next_stop

    def set_prev_stop(self, prev_stop):
        self.prev_stop = prev_stop

class MetroLine:
    def __init__(self, name):
        self.line_name = name
        self.node = None
        self.stops = []

    def get_line_name(self):
        return self.line_name

    def get_node(self):
        return self.node

    def set_node(self, node):
        self.node = node

    def print_line(self):
        stop = self.node
        while stop is not None:
            print(stop.get_stop_name())
            stop = stop.get_next_stop()

    def get_total_stops(self):
        stop = (self.node).get_next_stop()
        count = 0
        while stop is not None:
            count +=1
            stop = stop.get_next_stop()

        return count

    def populate_line(self, filename):
        line_name = filename[0:len(filename)-4]
        with open(filename,"r") as file:
            line = file.readline()
            line = line[0:len(line)-2]
            last_index = line.rfind(" ")
            prev_name = line[:last_index]
            self.stops.append(prev_name)
            prev_fare = line[last_index+1:]
            prev_stop = MetroStop(prev_name,line_name,prev_fare)
            self.set_node(prev_stop)
            line = file.readline()
            line = line[0:len(line)-2]
            last_index = line.rfind(" ")
            curr_name = line[:last_index]
            self.stops.append(curr_name)
            curr_fare = line[last_index+1:]
            curr_stop = MetroStop(curr_name,line_name,curr_fare)
            prev_stop.set_next_stop(curr_stop)
            curr_stop.set_prev_stop(prev_stop)
            prev_stop = curr_stop
            for line in file:
                if line:
                    line = line[0:len(line)-2]
                    last_index = line.rfind(" ")
                    curr_name = line[:last_index]
                    self.stops.append(curr_name)
                    curr_fare = line[last_index+1:]
                    curr_stop = MetroStop(curr_name,line_name,curr_fare)
                    prev_stop.set_next_stop(curr_stop)
                    curr_stop.set_prev_stop(prev_stop)
                    prev_stop = curr_stop

class AVLNode:
    def __init__(self, name):
        self.stop_name = name
        self.stops = []
        self.left = None
        self.right = None
        self.parent = None

    def get_stop_name(self):
        return self.stop_name

    def get_stops(self):
        return self.stops

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_parent(self):
        return self.parent

    def add_metro_stop(self, metro_stop):
        self.stops.append(metro_stop)

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def set_parent(self, parent):
        self.parent = parent

class AVLTree:
    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def set_root(self, root):
        self.root = root
        

    def height(self, node):
        if node is None:
            return 0
        left_height = self.height(node.left)
        right_height = self.height(node.right)
        return max(left_height, right_height) + 1


    def string_compare(self, s1, s2):
        if (s1 > s2) : return 1
        if (s1 == s2) : return 0
        if (s1 < s2 ) : return -1

    def balance_factor(self, node):
        if node is None:
            return 0
        left_height = self.height(node.get_left())
        right_height = self.height(node.get_right())
        return left_height - right_height


    def rotate_left(self, node):
        y = node.right
        node.right = y.left
        if y.left is not None:
            y.left.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root=y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y
        

    
    def rotate_right(self, node):
        y = node.left
        node.left = y.right
        if y.right is not None:
            y.right.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root=y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.right = node
        node.parent = y

    def balance(self,node):
        while node:
            if self.balance_factor(node) <-1 and node.right:
                if self.balance_factor(node.right) > 0:
                    self.rotate_right(node.right)
                self.rotate_left(node)
            elif self.balance_factor(node) > 1 and node.left:
                if self.balance_factor(node.left) < 0:
                    self.rotate_left(node.left)
                self.rotate_right(node)
            node = node.get_parent()

            
    def insert(self, node, metro_stop):
        if self.root is None:
            self.root = AVLNode(metro_stop.get_stop_name())
            self.root.add_metro_stop(metro_stop)
            return
        
        if metro_stop.get_stop_name() < node.get_stop_name():
            if node.get_left() is None:
                new_node = AVLNode(metro_stop.get_stop_name())
                new_node.add_metro_stop(metro_stop)
                node.set_left(new_node)
                new_node.set_parent(node)
            else:
                self.insert(node.get_left(), metro_stop)
        elif metro_stop.get_stop_name() > node.get_stop_name():
            if node.get_right() is None:
                new_node = AVLNode(metro_stop.get_stop_name())
                new_node.add_metro_stop(metro_stop)
                node.set_right(new_node)
                new_node.set_parent(node)
            else:
                self.insert(node.get_right(), metro_stop)
        else:
            node.add_metro_stop(metro_stop)
        
        self.balance(node)

    def populate_tree(self, metro_line):
        metro_stop = metro_line.node
        while metro_stop is not None:
            self.insert(self.root,metro_stop)
            metro_stop = metro_stop.get_next_stop()

    def in_order_traversal(self, node):
        if node is None:
            return
        self.in_order_traversal(node.get_left())
        self.in_order_traversal(node.get_right())

    def get_total_nodes(self, node):
        if node is None:
            return 0
        return 1 + self.get_total_nodes(node.get_left()) + self.get_total_nodes(node.get_right())

    def search_stop(self, stop_name):
        node = self.root
        while node and node.stop_name != stop_name:
            if node.stop_name < stop_name:
                node = node.right
            elif node.stop_name > stop_name:
                node = node.left
            else:
                return None
        return node
    
    def isJunction(self,stop_name):
        node = self.search_stop(stop_name)
        if(len(node.stops)) > 1:
            return True
        return False

class Trip:
    def __init__(self, metro_stop, previous_trip):
        self.node = metro_stop
        self.prev = previous_trip
        self.stop = None
        self.follow = []

    def get_node(self):
        return self.node

    def get_prev(self):
        return self.prev
    

class Exploration:
    def __init__(self):
        self.trips = []
        self.used = []

    def get_trips(self):
        return self.trips

    def enqueue(self, trip):
        self.trips.append(trip)

    def dequeue(self):
        if not self.trips:
            return None
        trip = self.trips.pop(0)
        self.used.append(trip)
        print("Dequeued:", trip.get_node().get_stop_name())
        return trip

    def is_empty(self):
        return not bool(self.trips)
    
    def noTrip(self,stop_name):
        for i in self.used:
            for j in self.trips:
                if i.node.stop_name == stop_name or j.node.stop_name == stop_name:
                    return False
        return True

class Path:
    def __init__(self):
        self.stops = []
        self.total_fare = 0

    def get_stops(self):
        return self.stops

    def get_total_fare(self):
        return self.total_fare

    def add_stop(self, stop):
        self.stops.append(stop)

    def set_total_fare(self, fare):
        self.total_fare = fare

    def print_path(self):
        for stop in self.stops:
            print(stop.get_stop_name())

    def calculate_fair(self):
        if len(self.stops) == 0 or len(self.stops) == 1:
            self.total_fare = 0
        else:
            self.stops = self.stops[::-1]
            curr = self.stops[2]
            for i in range(1,len(self.stops)):
                if self.stops[i].prev_stop and (self.stops[i].prev_stop != self.stops[i-1] or self.stops[i].next_stop != self.stops[i-1]):
                     if self.stops[i].prev_stop.stop_name == self.stops[i-1].stop_name:
                         self.total_fare += abs(int(self.stops[i].fare) - int(self.stops[i].prev_stop.fare))
                     else:
                        self.total_fare += abs(int(self.stops[i].fare) - int(self.stops[i].next_stop.fare))
                else:
                    self.total_fare += abs(int(self.stops[i].fare)-int(self.stops[i-1].fare))

            self.stops = self.stops[::-1]
                

class PathFinder:
    def __init__(self, avl_tree, metro_lines):
        self.tree = avl_tree
        self.lines = metro_lines

    def get_tree(self):
        return self.tree

    def get_lines(self):
        return self.lines

    def create_avl_tree(self):
        for line in lines:
            if self.tree.root is None:
                self.tree.set_root(AVLNode(line.stops[0]))
            self.tree.populate_tree(line)

    def find_path(self, origin, destination):
        origin_stops = self.tree.search_stop(origin).stops
        explore = Exploration()
        paths = []

        for i in range(len(origin_stops)):
            if origin_stops[i].next_stop:
                explore.enqueue(Trip(origin_stops[i].next_stop, None))
                explore.trips[-1].follow.append(origin_stops[i])
            if origin_stops[i].prev_stop:
                explore.enqueue(Trip(origin_stops[i].prev_stop, None))
                explore.trips[-1].follow.append(origin_stops[i])
        while not explore.is_empty():
            
            trip = explore.dequeue()
            metro_stop = trip.node
            
            while metro_stop and trip:

                if metro_stop.stop_name == destination:
                    trip.follow.append(metro_stop)
                    paths.append(Path())
                    while trip:
                        trip.follow = trip.follow[::-1]
                        paths[-1].stops = paths[-1].stops + trip.follow
                        trip = trip.prev
                    break
                
                else:
                    if self.tree.isJunction(metro_stop.stop_name):
                        trip.stop = metro_stop
                        trip.follow.append(metro_stop)
                        origin_stops = self.tree.search_stop(metro_stop.stop_name).stops
                        metro_stop = trip.follow[len(trip.follow)-2]
                        for i in range(len(origin_stops)):
                            if origin_stops[i].next_stop and origin_stops[i].next_stop != metro_stop:
                                if explore.noTrip(origin_stops[i].next_stop.stop_name):
                                    explore.enqueue(Trip(origin_stops[i].next_stop, trip))
                            if origin_stops[i].prev_stop and origin_stops[i].prev_stop != metro_stop:
                                if explore.noTrip(origin_stops[i].prev_stop.stop_name):
                                    explore.enqueue(Trip(origin_stops[i].prev_stop, trip))
                        break
                    else:
                        if len(trip.follow) == 0:
                            if trip.prev is None:
                                if metro_stop.prev_stop and metro_stop.prev_stop.stop_name == origin:
                                    trip.follow.append(metro_stop)
                                    metro_stop = metro_stop.next_stop
                                else:
                                    trip.follow.append(metro_stop)
                                    metro_stop = metro_stop.prev_stop
                            else:
                                if metro_stop.prev_stop and metro_stop.prev_stop.stop_name == trip.prev.stop.stop_name:
                                    trip.follow.append(metro_stop)
                                    metro_stop = metro_stop.next_stop
                                else:
                                    trip.follow.append(metro_stop)
                                    metro_stop = metro_stop.prev_stop
                        else:
                            f = trip.follow
                            if metro_stop.prev_stop and metro_stop.prev_stop.stop_name == f[-1].stop_name:
                                trip.follow.append(metro_stop)
                                metro_stop = metro_stop.next_stop
                            else:
                                trip.follow.append(metro_stop)
                                metro_stop = metro_stop.prev_stop
        print(len(paths))
        if  len(paths) != 0:
            ans_path = paths[0]
            for i in paths:
                if(len(i.stops)<len(ans_path.stops)):
                    ans_path = i
            ans_path.calculate_fair()
            return ans_path

        return None
lines = []