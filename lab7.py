class MaxHeap:
    def __init__(self):
        self.l = [None]

    def parent(self, i):
        return i // 2

    def left(self, i):
        return 2 * i

    def right(self, i):
        return 2 * i + 1

    def get_max(self):
        return self.l[1] if len(self.l) > 1 else None

    def extract_max(self):
        if len(self.l) == 1:
            return None

        max_item = self.l[1]
        if len(self.l) == 2:
            self.l.pop()
            return max_item
        self.l[1] = self.l.pop()
        self.max_heapify(1)

        return max_item

    def max_heapify(self, i):
        left_child = self.left(i)
        right_child = self.right(i)

        largest = i

        if left_child < len(self.l) and self.l[left_child].priority > self.l[largest].priority:
            largest = left_child

        if right_child < len(self.l) and self.l[right_child].priority > self.l[largest].priority:
            largest = right_child

        if largest != i:
            self.l[i], self.l[largest] = self.l[largest], self.l[i]
            self.max_heapify(largest)

    def insert(self, item):
        self.l.append(item)
        i = len(self.l) - 1
        while i > 1 and self.l[self.parent(i)].priority < self.l[i].priority:
            self.l[i], self.l[self.parent(i)] = self.l[self.parent(i)], self.l[i]
            i = self.parent(i)

    def is_empty(self):
        return len(self.l) == 1

class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = []
        self.min_freight_cars_to_move = 0
        self.max_parcel_capacity = 0
        self.complete = {}

    def add_edge(self, source, destination, min_freight_cars_to_move, max_parcel_capacity):
        self.min_freight_cars_to_move = min_freight_cars_to_move
        self.max_parcel_capacity = max_parcel_capacity
        if source in self.vertices:
            sv = self.vertices.get(source)
            m = 1
            for i in sv.neighbors:
                if i == destination:
                    m = 0
            if m:
                sv.add_neighbor(destination)

        else:
            sv = Vertex(source,min_freight_cars_to_move,max_parcel_capacity)
            self.vertices[source] = sv
            sv.add_neighbor(destination)
        if destination in self.vertices:
            dv = self.vertices.get(destination)
            m = 1
            for i in dv.neighbors:
                if i == source:
                    m = 0
            if m:
                dv.add_neighbor(source)
        else:
            dv = Vertex(destination,min_freight_cars_to_move,max_parcel_capacity)
            self.vertices[destination] = dv
            dv.add_neighbor(source)
        self.edges.append([sv,dv])

    def print_graph(self):
        for i in self.vertices:
            node = self.vertices.get(i)
            for j in node.neighbors:
                print(i,j)
            print()

    def bfs(self, source, destination):
        ans=[]
        q = []
        s = {}
        q.append(source)
        s[source] = None
        while len(q) != 0:
            node = q[0]
            q = q[1:len(q)]
            for i in self.vertices.get(node).neighbors:
                if i not in s:
                    q.append(i)
                    s[i] = node
        if destination not in s:
            return ans
        node = destination
        while node != source:
            ans = [node]+ans 
            node = s.get(node)
        ans = [node] + ans
        return ans

    def dfshelp(self,node,destination,l,temp,ans):
        temp.append(node)
        if(node==destination):
            ans.append(temp.copy())
            return
        
        for i in self.vertices.get(node).neighbors:
            if i not in l:
                l.append(i)
                self.dfshelp(i,destination,l,temp,ans)
                temp.pop()
                
    def dfs(self, source, destination):
        ans = []
        l = []
        temp = []
        l.append(source)
        self.dfshelp(source,destination,l,temp,ans)
        ans = ans[0]
        return ans

    def groupFreightCars(self):
        # group freight cars at every vertex based on their destination
        ans = {}
        vertices_copy = dict(self.vertices)
        for i in vertices_copy.values():
            i.clean_unmoved_freight_cars()
            i.loadFreightCars()
            for j in i.freight_cars:
                d = self.bfs(j.current_location, j.destination_city)
                if(len(d)) == 1:
                    if(j.move(j.current_location)):
                        del j
                    continue
                des = d[1]
                cur = j.current_location
                if (cur, des) not in ans:
                    ans[(cur, des)] = []
                ans[(cur, des)].append(j)
                j.next_link = des   
        # Create a copy of the keys to avoid modifying the dictionary during iteration
        ans_keys_copy = list(ans.keys())
        ans_copy = ans.copy()
        for i in ans_keys_copy:
            if len(ans[i]) < self.min_freight_cars_to_move:
                del ans_copy[i]
                l = ans[i]
                cur,des = i
                node = self.vertices[cur]
                d = self.dfs(cur, des)
                des = d[1]
                if (cur, des) not in ans_copy:
                    ans_copy[(cur, des)] = []
                for j in l:
                    ans_copy[(cur, des)].append(j)
                for k in l:
                    k.next_link = des
        ans = ans_copy.copy()            
        return ans


    def moveTrains(self):
        # move trains  (constitutes one time tick)
        # a train should move only if has >= min_freight_cars_to_move freight cars to link (link is a vertex, obtained from bfs or dfs)
        # once train moves from the source vertex, all the freight cars should be sealed and cannot be unloaded (at any intermediate station) until they reach their destination
        ans = self.groupFreightCars()
        for i in ans:
            l = ans[i].copy()
            cur,des = i
            node = self.vertices[cur]
            node_des = self.vertices[des]
            if(len(l)) >= self.min_freight_cars_to_move:
                for j in l:
                    j.visited.append(cur)
                    node.remove(j)
                    node_des.freight_cars.append(j)
                    node_des.sealed_freight_cars.append(j)
                    for k in j.parcels:
                        node_des.all_parcels.append(k)
                    if(j.move(des)):
                        del j

class Vertex:
    def __init__(self, name, min_freight_cars_to_move, max_parcel_capacity):
        self.name = name
        self.freight_cars = []
        self.neighbors = []
        self.trains_to_move = None
        self.min_freight_cars_to_move = min_freight_cars_to_move
        self.max_parcel_capacity = max_parcel_capacity
        self.parcel_destination_heaps = {}
        self.sealed_freight_cars = []
        self.all_parcels = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
    
    def get_all_current_parcels(self):
        return self.all_parcels
    
    def clean_unmoved_freight_cars(self):
        # remove all freight cars that have not moved from the current vertex
        # add all parcels from these freight cars back to the parcel_destination_heaps accoridingly
        temp = []
        for i in self.freight_cars:
            if i.sealed == False:
                for j in i.parcels:
                    self.loadParcel(j)
                del i
            else:
                temp.append(i)
        self.freight_cars = temp

    def loadParcel(self, parcel):
        # load parcel into parcel_destination_heaps based on parcel.destination
        self.all_parcels.append(parcel)
        name = parcel.destination
        if name not in self.parcel_destination_heaps:
            temp = MaxHeap()
            self.parcel_destination_heaps[name] = temp
        self.parcel_destination_heaps[name].insert(parcel)

    def loadFreightCars(self):
        # load parcels onto freight cars based on their destination
        # remember a freight car is allowed to move only if it has exactly max_parcel_capacity parcels
        for i in self.parcel_destination_heaps:
            h = self.parcel_destination_heaps[i]
            size = len(h.l)
            size = size - 1
            if(size%self.max_parcel_capacity==0):
                num = size//self.max_parcel_capacity
            else:
                num = size//self.max_parcel_capacity + 1
            for j in range(num):
                temp = FreightCar(self.max_parcel_capacity)
                for k in range(self.max_parcel_capacity):
                    if h.is_empty() == False:
                        top = h.extract_max()
                        temp.load_parcel(top)
                        temp.current_location = top.current_location
                        temp.destination_city = top.destination
                self.freight_cars.append(temp)
                    
    def remove(self,f):
        self.freight_cars.remove(f)
        for i in f.parcels:
            self.all_parcels.remove(i)
        if f.sealed:
            self.sealed_freight_cars.remove(f)
        else:
            f.sealed = True
        
class FreightCar:
    def __init__(self, max_parcel_capacity):

        self.max_parcel_capacity = max_parcel_capacity
        self.parcels = []
        self.destination_city = None
        self.next_link = None
        self.current_location = None
        self.sealed = False
        self.visited = []

    def load_parcel(self, parcel):
        # load parcel into freight car
        
        self.parcels.append(parcel)

    def can_move(self):
        # return True if freight car can move, False otherwise
        if len(self.parcels) < self.max_parcel_capacity:
            return False
        
    def move(self, destination):
        # update current_location
        # empty the freight car if destination is reached, set all parcels to delivered
        self.current_location = destination
        if self.destination_city == destination:
            for i in self.parcels:
                i.delivered = True
            self.parcels = [] 
            return True
        return False

class Parcel:
    def __init__(self, time_tick, parcel_id, origin, destination, priority):
        self.time_tick = time_tick
        self.parcel_id = parcel_id
        self.origin = origin
        self.destination = destination
        self.priority = priority
        self.delivered = False
        self.current_location = origin

class PRC:
    def __init__(self, min_freight_cars_to_move=5, max_parcel_capacity=5):
        self.graph = Graph()
        self.freight_cars = []
        self.parcels = {}
        self.parcels_with_time_tick = {}
        self.min_freight_cars_to_move = min_freight_cars_to_move
        self.max_parcel_capacity = max_parcel_capacity
        self.time_tick = 1
        self.old_state = None
        self.new_state = None
        self.max_time_tick = 10
    
    def get_state_of_parcels(self):
        return {x.parcel_id:x.current_location for x in self.parcels.values()}
        
    def process_parcels(self, booking_file_path):
        with open(booking_file_path,"r") as f:
            lines = f.readlines()
            for line in lines:
                time,pid,source,destination,p = line.split()
                p = int(p)
                time = int(time)
                if time not in self.parcels_with_time_tick:
                    self.parcels_with_time_tick[time] = [pid]
                else:
                    temp=self.parcels_with_time_tick.get(time)
                    temp.append(pid)
                    self.parcels_with_time_tick[time] = temp
                temp = Parcel(time,pid,source,destination,p)
                self.parcels[pid] = temp

    def getNewBookingsatTimeTickatVertex(self, time_tick, vertex):
        # return all parcels at time tick and vertex
        time_tick = int(time_tick)
        bookings = []
        node = self.parcels_with_time_tick.get(time_tick)
        for i in node:
            if self.parcels.get(i).current_location == vertex:
                bookings.append(self.parcels.get(i))
        return bookings

    def run_simulation(self, run_till_time_tick=None):
        max_tick_time = max(self.parcels_with_time_tick.keys())

        if run_till_time_tick is None:
            run_till_time_tick = max_tick_time

        if max_tick_time < run_till_time_tick:
            run_till_time_tick = max_tick_time

        self.time_tick = 0
        old_state = set()  # Set to store parcel IDs along with their current locations

        while run_till_time_tick:
            self.graph.moveTrains()
            self.time_tick += 1
            run_till_time_tick -= 1

            if self.time_tick <= max_tick_time:
                current_state = set()
                l = self.parcels_with_time_tick[self.time_tick]

                for i in l:
                    n = self.parcels[i]
                    current_state.add((n.parcel_id, n.current_location))
                    cur = n.origin
                    node = self.graph.vertices[cur]
                    node.loadParcel(n)

                # Check for convergence
                if self.convergence_check(old_state, current_state):
                    break

                old_state = current_state

    def convergence_check(self, previous_state, current_state):
        # Check if the sets of parcel IDs along with their current locations are the same
        return previous_state == current_state

    def all_parcels_delivered(self):
        return all(parcel.delivered for _,parcel in self.parcels.items())
    
    def get_delivered_parcels(self):
        return [parcel.parcel_id for parcel in self.parcels.values() if parcel.delivered]
    
    def get_stranded_parcels(self):
        return [parcel.parcel_id for parcel in self.parcels.values() if not parcel.delivered]

    def status_of_parcels_at_time_tick(self, time_tick):
        return [(parcel.parcel_id, parcel.current_location, parcel.delivered) for parcel in self.parcels.values() if parcel.time_tick <= time_tick and not parcel.delivered]
    
    def status_of_parcel(self, parcel_id):
        return self.parcels[parcel_id].delivered, self.parcels[parcel_id].current_location

    def get_parcels_delivered_upto_time_tick(self, time_tick):
        return [parcel.parcel_id for parcel in self.parcels.values() if parcel.time_tick <= time_tick and parcel.delivered]

    def create_graph(self, graph_file_path):
        with open(graph_file_path,"r") as f:
            lines = f.readlines()
            for line in lines:
                a,b = line.split()
                self.graph.add_edge(a,b,self.min_freight_cars_to_move,self.max_parcel_capacity) 
