# Course: 3642
# Student name: Brian Truong
# Student ID: 761964
# Assignment number: 2
# Due Date: 10/17/21
# Signature: Brian Truong

import time
import heapq
import copy
import sys
import pdb
import numpy as np

# dictionary associates string name of moves to coordinate counterparts
moves = {"left": [0, -1], "right": [0, 1], "up": [-1, 0], "down": [1, 0]}
# list of strings used in order to easily access string names for moves
move_names = [key for key in moves]
# max depth of search
d = 200
# given goal state
goal_state = np.array([[1, 2, 3],
                       [8, 0, 4],
                       [7, 6, 5]])


# used to create open list/frontier
class PriorityQueue:

    def __init__(self):
        self.pq = []

    def push(self, k):
        heapq.heappush(self.pq, k)

    def __len__(self):
        return len(self.pq)

    def pop(self):
        return heapq.heappop(self.pq)

    def is_empty(self):
        if not self.pq:
            return True
        else:
            return False

    # sorts pq by node cost
    def sort(self):
        return self.pq.sort(key=lambda c: c.cost)

    def clear(self):
        return self.pq.clear()

    def remove(self, k):
        return self.pq.remove(k)


# node class: represents 3 x 3 tile state configuration. neighbors of current node are all possible moves of 0 tile
# cursor represents position of 0 in puzzle, cost is heuristic value
class Node:

    def __init__(self, state, cursor, parent=None, h_val=0, g_val=0):
        self.parent = parent
        self.state = state
        self.cursor = cursor
        self.cost = h_val
        self.depth = g_val

    # defined so that nodes can be compared to each other by cost
    def __lt__(self, other):
        return self.cost < other.cost


# from a given state, calculate manhattan distance between state and goal
def heuristic1(m1, m2):
    count = 0
    for x in range(len(m1)):
        for y in range(len(m2)):
            ele = m1[x][y]
            goal_ele = np.where(m2 == ele)
            gx, gy = goal_ele[0], goal_ele[1]
            goal_ind = [gx[0], gy[0]]
            c = abs(x - goal_ind[0]) + abs(y - goal_ind[1])
            count += c
    return pow(count, 2)


# determines if moving 0 tile is legal at current position and given a move
def legal_move(x, y):
    if 0 <= x < 3 and 0 <= y < 3:
        return True
    return False


# compares the states of two nodes and returns true if they are the same
def same_state(node1, node2):
    comparison = node1.state == node2.state
    result = comparison.all()
    return result


# given node, get nodes cursor position and check legal moves from that position
# pend_move is a string representing direction cursor is moving
def move_cursor(s: Node, pend_move):
    # creates new state that is a copy of the parent node's state so that pend_move can be applied
    child_state = copy.deepcopy(s.state)
    init_pos = s.cursor
    move = moves[pend_move]
    new_pos = [x + y for x, y in zip(init_pos, move)]
    if legal_move(new_pos[0], new_pos[1]):
        # swaps position of 0 and number at the pending move
        child_state[init_pos[0]][init_pos[1]], child_state[new_pos[0]][new_pos[1]] = child_state[new_pos[0]][
                                                                                         new_pos[1]], \
                                                                                     child_state[init_pos[0]][
                                                                                         init_pos[1]]
        # returns puzzle state of child of node and new cursor position
        result = [child_state, new_pos]
        return result
    else:
        # case for when move is illegal
        return -1


# creates and returns new node after the cursor(0) has been moved
# new node has updated game state, cost derived from heuristic it's on
def new_node(n: Node, next_move):
    # if move is illegal, returns node that has identical state and cursor position as it's parent and an "infinite"
    # cost
    if move_cursor(n, next_move) == -1:
        child_node = Node(n.state, n.cursor, n, sys.maxsize)
        return child_node
    else:
        child_state = move_cursor(n, next_move)
        child_node = Node(child_state[0], child_state[1], n, heuristic1(child_state[0], goal_state))
        return child_node


# returns solution path
def print_path(n):
    solution = []
    solution.append(n.parent)
    while solution[-1] is not None:
        solution.append(solution[-1].parent)
    solution.remove(None)
    return solution


# implements greedy best first search
def gbfs(n):
    # create frontier, explored/closed list, and push the root node to the frontier
    start_time = time.time()
    frontier = PriorityQueue()
    explored = []
    goal_node = Node(goal_state, [1, 1], 0)
    root = n
    frontier.push(root)

    i = 0
    # iterates through search until depth limit is reached
    for i in range(d):
        # checks if there are no more possible children to be created, signaling failure
        if frontier.is_empty():
            print("A solution could not be found or maximum iterations were met")
            break
        # pops cheapest node to closed list and chooses most recent entry in closed list to expand children from
        explored.append(frontier.pop())
        next_node = explored[i]
        # if the latest node has the same state as goal state, goal has been reached
        # return sequence of moves to reach the goal, number of nodes visited, and computational time
        if same_state(explored[i], goal_node):
            end_time = time.time() - start_time
            nodes_visited = len(explored)
            result = "GBFS final path"
            final = []
            final.extend(print_path(explored[i]))
            final.reverse()
            final.append(goal_node)
            for s in range(len(final)):
                print(final[s].state)
            result += "\n number of nodes visited = %d \n computational time = %f" % (nodes_visited, end_time)
            return result

        # for all moves
        for m in move_names:
            # generate and push node based on current move
            child = new_node(next_node, str(m))
            frontier.push(child)
            # checks if child's state already exists in closed list
            # if true remove that child as to avoid possible cycles
            # also removes nodes that are illegal moves since any child node
            # that is an illegal move has the same state as it's parent
            for j in range(len(explored)):
                if same_state(child, explored[j]):
                    frontier.remove(child)
        # re sorts frontier in case removing a node disrupted order
        frontier.sort()
    # used for debugging
    print("\n\ngbfs: explored nodes")
    for a in range(len(explored)):
        final_path = []
        final_path.append(explored[a].state)
        print([explored[a].state, explored[a].cost], explored[a].cursor, i)
    print("\n\ngbfs: frontier \n\n")
    for b in range(len(frontier.pq)):
        print([frontier.pq[b].state, frontier.pq[b].cost], i)


# implements UCS
# identical to previous two searches except cost is determined only by g(n) or step cost
def ucs(n):
    start_time = time.time()
    frontier = PriorityQueue()
    explored = []
    goal_node = Node(goal_state, [1, 1], 0)
    root = n
    frontier.push(root)

    i = 0
    for i in range(d):
        if frontier.is_empty():
            print("A solution could not be found or maximum iterations were met")
            break

        explored.append(frontier.pop())
        next_node = explored[i]
        if same_state(explored[i], goal_node):
            end_time = time.time() - start_time
            nodes_visited = len(explored)
            result = "UCS final path"
            final = []
            final.extend(print_path(explored[i]))
            final.reverse()
            final.append(goal_node)
            for s in range(len(final)):
                print(final[s].state)
            result += "\n number of nodes visited = %d \n computational time = %f" % (nodes_visited, end_time)
            return result

        for m in move_names:
            child = new_node(next_node, str(m))
            child.cost = i
            frontier.push(child)
            for j in range(len(explored)):
                if same_state(child, explored[j]):
                    frontier.remove(child)

    print("\n\nUCS: explored nodes")
    for a in range(len(explored)):
        print([explored[a].state, explored[a].cost], explored[a].cursor)
    print("\n\nUCS: frontier \n\n")
    for b in range(len(frontier.pq)):
        print([frontier.pq[b].state, frontier.pq[b].cost], i)


# implements a* search
# identical to GBFS except the depth is added to each child's cost
def a_star(n):
    start_time = time.time()
    frontier = PriorityQueue()
    explored = []
    goal_node = Node(goal_state, [1, 1], 0)
    root = n
    frontier.push(root)

    for i in range(d):
        if frontier.is_empty():
            print("A solution could not be found or maximum iterations were met")
            break

        explored.append(frontier.pop())
        next_node = explored[i]

        if same_state(explored[i], goal_node):
            end_time = time.time() - start_time
            nodes_visited = len(explored)
            result = "a* final path"
            final = []
            final.extend(print_path(explored[i]))
            final.reverse()
            final.append(goal_node)
            for s in range(len(final)):
                print(final[s].state)
            result += "\n number of nodes visited = %d \n computational time = %f" % (nodes_visited, end_time)
            return result

        for m in move_names:
            child = new_node(next_node, str(m))
            child.depth = i
            child.cost += child.depth
            frontier.push(child)
            for j in range(len(explored)):
                if same_state(child, explored[j]):
                    frontier.remove(child)
                    # breakpoint()

        frontier.sort()

    print("\n\na*: explored nodes")
    for a in range(len(explored)):
        print([explored[a].state, explored[a].cost], explored[a].cursor, explored[a].depth)
    print("\n\na*: frontier \n\n")
    for b in range(len(frontier.pq)):
        print([frontier.pq[b].state, frontier.pq[b].cost], frontier.pq[b].depth)


# given initial state
init_state1 = np.array([[2, 8, 3],
                        [1, 6, 4],
                        [7, 0, 5]])
# easy initial state
init_state2 = np.array([[1, 3, 4],
                        [8, 6, 2],
                        [7, 0, 5]])
# medium initial state
init_state3 = np.array([[1, 3, 4],
                        [8, 0, 5],
                        [7, 2, 6]])
init_state4 = np.array([[1, 3, 4],
                        [8, 6, 2],
                        [0, 7, 5]])
init_state5 = np.array([[3, 6, 4],
                        [0, 1, 2],
                        [8, 7, 5]])

# calculates initial cost each puzzle
c1 = heuristic1(init_state1, goal_state)
c2 = heuristic1(init_state2, goal_state)
c3 = heuristic1(init_state3, goal_state)
c4 = heuristic1(init_state4, goal_state)
c5 = heuristic1(init_state5, goal_state)
# creates nodes for each respective puzzle
n1 = Node(init_state1, [2, 1], None, c1)
n2 = Node(init_state2, [2, 1], None, c2)
n3 = Node(init_state3, [1, 1], None, c3)
n4 = Node(init_state4, [2, 0], None, c4)
n5 = Node(init_state5, [1, 0], None, c5)

# function calls
print(ucs(n1))
print(gbfs(n1))
print(a_star(n1))
