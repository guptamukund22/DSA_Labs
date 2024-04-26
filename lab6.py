import re
class HybridNode:
    def __init__(self, key, element):
        self.key = key  # Key
        self.element = element  # Element
        self.parent = None  # Parent node
        self.left_child = None  # Left child node
        self.right_child = None  # Right child node
        self.next_node = None  # Next node in the linked list
        self.prev_node = None
        self.color = "red"  # "red" or "black"
        self.mru = None

class MRU:
    def __init__(self,key,element):
        self.key = key
        self.element = element
        self.count = 1
        self.next = None
        self.prev = None
        self.node = None

class RedBlackTree:
    def __init__(self):
        self.root = None
        self.head = None
    
    def search(self, key):
        x = self.root
        while x and x.key != key:
            if x.key<key:
                x = x.right_child
            else:
                x = x.left_child
        if x is not None:
            while x.prev_node is not None:
                x = x.prev_node
        return x
    
    def traverse_up(self, x):
        L = []
        while x is not None:
            L.append(x) 
            x = x.parent
        return L
    
    def traverse_down(self, x, bit_sequence):
        L = []
        x = self.root
        bit_sequence = str(bit_sequence)
        for i in bit_sequence:
            L.append(x)
            if x is None:
                pass
            elif i == "1":
                x = x.left_child
            elif i == "0":
                x = x.right_child
        return L

    def right_rotate(self,x):
        w = x.left_child
        x.left_child = w.right_child
        if w.right_child:
            w.right_child.parent = x
        w.parent = x.parent
        if x.parent:
            if x.parent.left_child == x:
                x.parent.left_child = w
            else:
                x.parent.right_child = w
        else:
            self.root = w
        
        w.right_child = x
        x.parent = w
        return w
    
    def left_rotate(self,x):
        w = x.right_child
        x.right_child = w.left_child
        if w.left_child:
            w.left_child.parent = x
        w.parent = x.parent
        if x.parent:
            if x.parent.left_child == x:
                x.parent.left_child = w
            else:
                x.parent.right_child = w
        else:
            self.root = w
        w.left_child = x
        x.parent = w
        return w
    
    def black_height(self, node):  
        height = 0
        x = self.root
        while x is not None:
            if x.color == "black":
                height +=1
            x = x.left_child
        return height 

    def insert_fixup(self,x):
        while x.parent and x.parent.color =="red":
            if x.parent.parent and x.parent.parent.right_child == x.parent:
                y = x.parent.parent.left_child
                if y and  y.color == "red":
                    y.color = "black"
                    x.parent.color = "black"
                    x.parent.parent.color = "red"
                    x = x.parent.parent
                else:
                    if x.parent.left_child == x:
                        x = x.parent
                        x = self.right_rotate(x)
                        x= x.right_child
                    x.parent.color = "black"
                    x.parent.parent.color = "red"
                    self.left_rotate(x.parent.parent)
            elif x.parent.parent and x.parent.parent.left_child == x.parent:
                y = x.parent.parent.right_child
                if y and y.color == "red":
                    y.color = "black"
                    x.parent.color = "black"
                    x.parent.parent.color="red"
                    x= x.parent.parent
                else:
                    if x.parent.right_child == x:
                        x = x.parent
                        x=self.left_rotate(x)
                        x = x.left_child
                    x.parent.color = "black"
                    x.parent.parent.color= "red"
                    self.right_rotate(x.parent.parent)
        self.root.color = "black"
                
    def insert(self, key, element):  
        if self.root == None:
            self.root = HybridNode(key,element)
            self.root.mru = MRU(key,element)
            self.root.mru.node = self.root
            self.head = self.root.mru
            self.insert_fixup(self.root)
            return self.root
        x = self.root
        y = self.root
        while x is not None:
            if x.key == key:
                while x.prev_node != None:
                    x = x.prev_node
                y = x
                while x is not None and x.element != element:
                    y = x
                    x = x.next_node 
                if x is None:
                    y.next_node = HybridNode(key,element)
                    y.next_node.color = y.color
                    y.next_node.prev_node = y
                    y.next_node.mru = MRU(key,element)
                    y.next_node.mru.node = y.next_node
                    y.next_node.mru.next = self.head
                    self.head.prev = y.next_node.mru
                    self.head = y.next_node.mru
                    y.next_node.mru.count = 0
                    x = y.next_node
                x.mru.count += 1
                if x.mru != self.head:
                    x.mru.prev.next = x.mru.next
                    if x.mru.next:
                        x.mru.next.prev = x.mru.prev

                    x.mru.next = self.head
                    self.head.prev = x.mru
                    self.head = x.mru
                    self.head.prev = None
                break
            else:
                if x.key < key:
                    y=x
                    x = x.right_child
                else:
                    y=x
                    x = x.left_child
        if x == None:
            x = y
            if key > x.key:
                x.right_child = HybridNode(key,element)
                x.right_child.mru = MRU(key,element)
                x.right_child.mru.node = x.right_child
                x.right_child.parent = x
                self.head.prev = x.right_child.mru
                x.right_child.mru.next = self.head
                self.head = x.right_child.mru
                x = x.right_child
            else:
                x.left_child = HybridNode(key,element)
                x.left_child.mru = MRU(key,element)
                x.left_child.mru.node = x.left_child
                x.left_child.parent = x
                self.head.prev = x.left_child.mru
                x.left_child.mru.next = self.head
                self.head = x.left_child.mru
                x = x.left_child
            y = self.search(key)
            while y.next_node is not None and y.element != x.element:
                y = y.next_node
            if y.element != x.element:
                y.next_node = x
                x.prev_node = y
            self.insert_fixup(x)
        return x
    
    def minimum(self,x):
        y = x
        while x is not None:
            y = x
            x = x.left_child
        return y

    def height(self,node):
        if node is None:
            return - 1
        
        return 1+ max(self.height(node.left_child),self.height(node.right_child))

    def depth(self,node):
        if node is None:
            return -1
        d = 0
        temp = self.root
        while temp is not None and temp != node:
            d +=1
            if temp.key > node.key:
                temp = temp.left_child
            else:
                temp = temp.right_child
        return d
        

    def preorder_traversal(self, node, depth, result):
        if node is None:
            return result
        if self.depth(node) > depth:
            return result
        result.append(node)
        self.preorder_traversal(node.left_child,depth,result)
        self.preorder_traversal(node.right_child,depth,result)
        return result
    
    def delete_fixup(self,x,parent):
        if parent is None:
            self.root = x
            return
        
        while x != self.root and (x is None or x.color == "black") and parent is not None:
            if parent.left_child == x and parent.right_child != None:
                w = parent.right_child
                if w.color == "red":
                    w.color = "black"
                    parent.color = "red"
                    w = self.left_rotate(parent)
                    w = parent.right_child
                elif (w.right_child == None and w.left_child is None) or (w.left_child is None and w.right_child and w.right_child.color == "black") or (w.right_child is None and w.left_child and w.left_child.color == "black"):
                    w.color = "red"
                    x = parent
                    parent = parent.parent
                else:
                    if w.right_child and w.right_child.color == "red":
                        w.color = parent.color
                        parent.color = "black"
                        w.right_child.color = "black"
                        w = self.left_rotate(parent)
                        x = self.root
                    elif  w.left_child and w.left_child.color == "red":
                        if w.left_child == None:
                            break
                        w.left_child.color = "black"
                        w.color = "red"
                        w = self.right_rotate(w)
                        w = parent.right_child
                        w.color = parent.color
                        parent.color = "black"
                        w.right_child.color = "black"
                        w = self.left_rotate(parent)
                        x = self.root
            elif parent.right_child == x and parent.left_child !=None:
                w = parent.left_child
                if w.color == "red":
                    w.color = "black"
                    parent.color = "red"
                    w = self.right_rotate(parent)
                    w = parent.left_child
                elif (w.right_child == None and w.left_child is None) or (w.left_child is None and w.right_child and w.right_child.color == "black") or (w.right_child is None and w.left_child and w.left_child.color == "black"):
                    w.color = "red"
                    x = parent
                    parent = parent.parent
                else:
                    if w.left_child and w.left_child.color == "red":
                        w.color = parent.color
                        parent.color = "black"
                        w.left_child.color = "black"
                        w = self.right_rotate(parent)
                        x = self.root
                    elif  w.right_child and w.right_child.color == "red" and w.right_child:
                        w.right_child.color = "black"
                        w.color = "red"
                        w = self.left_rotate(w)
                        w = parent.left_child
                        w.color = parent.color
                        parent.color = "black"
                        w.left_child.color = "black"
                        w = self.right_rotate(parent)
                        x = self.root
                    
        x.color = "black"

    def delete(self,key):
        node = self.search(key)
        if node is None:
            return False
        if node.left_child is None and node.right_child is None:
            if node == self.root:
                self.root = None
            else:
                if node.parent.left_child == node:
                    node.parent.left_child = None
                else:
                    node.parent.right_child = None
            if node.color == "black":
                self.delete_fixup(node.right_child,node.parent)

        elif node.left_child is None:
            if node.parent.right_child == node:
                node.parent.right_child = node.right_child
            else:
                node.parent.left_child = node.right_child
            if node.right_child:
                node.right_child.parent = node.parent
            if node.color == "black":
                self.delete_fixup(node.right_child,node.parent)

        elif node.right_child is None:
            if node.parent.right_child == node:
                node.parent.right_child = node.left_child
            else:
                node.parent.left_child = node.left_child
            if node.left_child:
                node.left_child.parent = node.parent
            if node.color == "black":
                self.delete_fixup(node.left_child,node.parent)

        else:
            y = self.minimum(node.right_child)
            x = y.right_child
            if y.parent == node:
                node.right_child = x
                if x:
                    x.parent = node
            else:
                y.parent.left_child = x
                if x:
                    x.parent = y.parent
            node.key = y.key
            node.element = y.element
            node.next_node = y.next_node
            node.prev_node = y.prev_node
            node.mru = y.mru
            if y.color == "black":
                self.delete_fixup(x,y.parent)
        return True

class Lexicon:
    def __init__(self):
        self.red_black_tree = RedBlackTree()
        self.num_of_chap = 0  
        self.chapter_list = []

    def read_chapters(self, chapter_names):
        self.chapter_list += chapter_names
        self.num_of_chap += len(chapter_names)
        for chapter in chapter_names:
            with open(chapter, 'r') as f:
                content = f.read()      
                words = re.split(r'[.,!? ]', content)
                words = [word for word in words if word !=""]
                for word in words:
                    processed_word = word.strip().lower()
                    if processed_word:  
                        self.red_black_tree.insert(processed_word, chapter)
            
    def prune(self,node):
        if node is None:
            return 
        
        if node.left_child:
            self.prune(node.left_child)

        if node.right_child:
            self.prune(node.right_child)
        count = 0
        temp = node
        while temp is not None:
            count +=1
            temp = temp.next_node
        if count == self.num_of_chap:
            self.red_black_tree.delete(node.key)

    
    def build_index_help(self,node,L):
        if node is None:
            return L
        if node.left_child:
            L=self.build_index_help(node.left_child,L)
        if node.right_child:
            L=self.build_index_help(node.right_child,L)
        i = 0
        while i < len(L) and L[i].word < node.key:
            i +=1
        temp = node
        m = IndexEntry(temp.key)
        for i in range(self.num_of_chap):
            if temp and temp.element == self.chapter_list[i]:
                m.chapter_word_counts.append([temp.element, temp.mru.count])
                temp = temp.next_node 
            else:
                m.chapter_word_counts.append([self.chapter_list[i], 0])
        L.insert(i,m)
        return L    

    def build_index(self):
        self.prune(self.red_black_tree.root)
        self.prune(self.red_black_tree.root)
        L = []
        L = self.build_index_help(self.red_black_tree.root,L)
        L = sorted(L,key = lambda entry:entry.word)
        return L

class IndexEntry:
    def __init__(self, word):
        self.word = word  # Word
        self.chapter_word_counts = []  # List of (chapter, word_count) tuples