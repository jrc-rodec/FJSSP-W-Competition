import copy
import random
import numpy as np
import statistics

def run_n_simulations(s, e, m, w, js, d, uncertainty_parameters, n_simulations, uncertainty_source : str = 'worker'):
    results = []
    for i in range(n_simulations):
        g = Graph(s, e, m, w, js)
        g.simulate(d, uncertainty_parameters, uncertainty_source=uncertainty_source)
        results.append(float(max(g.e)))

    robust_makespan = statistics.mean(results)
    robust_makespan_stdev = statistics.stdev(results)
    R = robust_makespan/max(e)
    return results, robust_makespan, robust_makespan_stdev, R


class Graph:

    def __init__(self, s, e, a, w, js, leftshift : bool = False, buffers : list[float] = []):
        self.roots = []
        self.leftshift = leftshift
        self.js = copy.deepcopy(js)
        self.s = copy.deepcopy(s)
        self.e = copy.deepcopy(e)
        self.m = copy.deepcopy(a)
        self.w = copy.deepcopy(w)
        Node.leftshift = leftshift
        if len(buffers) == 0:
            buffers = [0] * len(s)
        self.b = copy.deepcopy(buffers)
        nodes = []
        for i in range(len(s)):
            nodes.append(Node(self.s, self.e, self.m, self.w, self.js, self.b, i))
        for i in range(len(nodes)):
            nodes[i].add_neighbours(self.m, self.w, self.js, nodes, i)
            if len(nodes[i].parents) == 0:
                self.roots.append(nodes[i])
        self.all_nodes = nodes

    def get_vectors(self):
        s = []
        e = []
        m = []
        w = []
        b = []
        for i in range(len(self.all_nodes)):
            s.append(self.all_nodes[i].start)
            e.append(self.all_nodes[i].end)
            m.append(self.all_nodes[i].machine)
            w.append(self.all_nodes[i].worker)
            b.append(self.all_nodes[i].buffer)
        return s, e, m, w, b

    def add_child(self, current, open_list, closed_list):
        in_open = current in open_list
        in_closed = current in closed_list
        if in_open or in_closed:
            return
        for parent in current.parents:
            if parent not in open_list and parent not in closed_list:
                self.add_child(parent, open_list, closed_list)
        open_list.append(current)

    def real_duration(self, d, wv):
        du = d*wv[2] + d*random.betavariate(wv[0], wv[1]) # get real duration
        return du
    
    def update(self):
        open_list = []
        closed_list = []
        open_list.extend(self.roots)
        while len(open_list) > 0:
            current : Node = open_list.pop(0)
            closed_list.append(current)
            for child in current.children:
                self.add_child(child, open_list, closed_list)
            current.update_values()
        n_ops = len(self.e)
        for i in range(n_ops):
            self.s[i] = self.all_nodes[i].start
            self.b[i] = self.all_nodes[i].buffer
            self.e[i] = self.all_nodes[i].end

    def simulate(self, d, wv : list = [], uncertainty_source : str = 'worker'):
        d = copy.deepcopy(d)
        machine_uncertainty = uncertainty_source == 'machine'
        single_distribution = uncertainty_source == 'single'
        if wv != None:
            for i in range(len(d)):
                for j in range(len(d[i])):
                    for k in range(len(d[i][j])):
                        d[i][j][k] = self.real_duration(d[i][j][k], wv[k] if not machine_uncertainty else wv[0] if single_distribution else wv[j]) # ignores 0s automatically
        open_list = []
        closed_list = []
        open_list.extend(self.roots)
        while len(open_list) > 0:
            current : Node = open_list.pop(0)
            closed_list.append(current)
            for parent in current.parents: # should not be necessary
                if parent not in closed_list:
                    print('something went wrong')
            for child in current.children:
                self.add_child(child, open_list, closed_list)
            current.update_time_slot(d)
        self.update()

    def get_predecessors(self, node):
        open_list = [node]
        closed_list = []
        while len(open_list) > 0:
            current = open_list.pop(0)
            closed_list.append(current)
            for parent in current.parents:
                if parent not in open_list and parent not in closed_list:
                    open_list.append(parent)
        return closed_list

    def get_successors(self, node):
        open_list = [node]
        closed_list = []
        while len(open_list) > 0:
            current = open_list.pop(0)
            closed_list.append(current)
            for child in current.children:
                if child not in open_list and child not in closed_list:
                    open_list.append(child)
        return closed_list
    
    def count_parents(self, node):
        return len(self.get_predecessors(node))

    def count_children(self, node):
        return len(self.get_successors(node))

    def get_makespan(self):
        pass

    def plot_data(self, strict : bool = False):
        s = []
        e = []
        m = []
        b = []
        jb = []
        w = []
        l = []
        pre = []
        suc = []
        sequence = []
        c = max([node.end for node in self.all_nodes])
        c_nodes = [node for node in self.all_nodes if node.end == c]
        n_machines = len(list(set([node.machine for node in self.all_nodes])))
        n_workers = len(list(set([node.worker for node in self.all_nodes])))
        crit_nodes = []
        for node in c_nodes:
            crit_nodes.append(node)
            if not strict:
                predecessors = self.get_predecessors(node)
                for predecessor in predecessors:
                    if predecessors not in crit_nodes:
                        crit_nodes.append(predecessor)
            else:
                predecessors = [parent for parent in node.parents]
                while len(predecessors) > 0:
                    most_critical = [predecessors.pop(0)]
                    for parent in predecessors:
                        if node.start-parent.end < node.start-most_critical[0].end:
                            most_critical = [parent]
                        elif node.start-parent.end == node.start-most_critical[0].end:
                            most_critical.append(parent)
                    predecessors = []
                    for parent in most_critical:
                        if parent not in crit_nodes:
                            crit_nodes.append(parent)
                            predecessors.extend(parent.parents)
        is_critnode = [True if node in crit_nodes else False for node in self.all_nodes]
        for i in range(len(self.all_nodes)):
            s.append(self.all_nodes[i].start)
            e.append(self.all_nodes[i].end)
            m.append(self.all_nodes[i].machine)
            b.append(self.all_nodes[i].buffer)
            jb.append(self.all_nodes[i].job)
            w.append(self.all_nodes[i].worker)
            pre.append(self.count_parents(self.all_nodes[i]))
            suc.append(self.count_children(self.all_nodes[i]))
            
            l.append([])
            for child in self.all_nodes[i].children:
                l[-1].append([e[-1],child.start, m[-1], child.machine])
            sequence.append(self.all_nodes[i].operation)
        js = sorted(sequence, key=lambda x: s[x])
        on_machine = []
        for i in range(n_machines): # n machines
            machine = []
            for j in range(len(js)):
                if m[j] == i:
                    machine.append(j)
            machine.sort(key=lambda x: s[x])
            on_machine.append(machine)
        same_worker = []
        for i in range(n_workers): # n workers
            worker = []
            for j in range(len(js)):
                if w[j] == i:
                    worker.append(j)
            worker.sort(key=lambda x: s[x])
            same_worker.append(worker)
        job_sequence = []
        for i in range(len(set(js))):
            job = [0] * len(js)
            for j in range(js.index(i), js.index(i)+js.count(i)):
                operation = j-js.index(i)
                n_operations = js.count(i)
                job[j] = n_operations-operation-1
            job_sequence.append(job)
        return s, e, m, w, b, jb, l, pre, suc, job_sequence, on_machine, same_worker, is_critnode

class Node:

    leftshift = False

    def __init__(self, s, e, m, w, js, b, i):
        self.start = s[i]
        self.end = e[i]
        self.job = js[i]
        self.machine = m[i]
        self.worker = w[i]
        self.parents = []
        self.children = []
        self.buffer = b[i]*(self.end-self.start)
        
        self.operation = i

    def add_neighbours(self, m, w, js, nodes, i):
        if i > 0 and js[i-1] == js[i]:
            self.parents.append(nodes[i-1])
        if i+1 < len(js) and js[i+1] == js[i]:
            self.children.append(nodes[i+1])
        on_machine = [j for j in range(len(m)) if m[j] == m[i]]
        on_machine.sort(key=lambda x: nodes[x].start)
        mi = on_machine.index(i)
        if mi > 0:
            idx = mi-1
            while idx >= 0 and nodes[on_machine[idx]].start == nodes[on_machine[mi]].start:
                idx-=1
            if nodes[on_machine[idx]].start != nodes[on_machine[mi]].start:
                self.parents.append(nodes[on_machine[idx]])
        if mi+1 < len(on_machine):
            self.children.append(nodes[on_machine[mi+1]])
        same_worker = [j for j in range(len(w)) if w[j] == w[i]]
        same_worker.sort(key=lambda x: nodes[x].start)
        wi = same_worker.index(i)
        if wi > 0:
            idx = wi-1
            while idx >= 0 and nodes[same_worker[idx]].start == nodes[same_worker[wi]].start:
                idx-=1
            if nodes[same_worker[idx]].start != nodes[same_worker[wi]].start:

                self.parents.append(nodes[same_worker[idx]])
        if wi+1 < len(same_worker):
            self.children.append(nodes[same_worker[wi+1]])

    def update_values(self):
        s = self.start
        e = self.end
        d = e-s
        parent_end_times = [parent.end + parent.buffer for parent in self.parents]
        parent_end_times.append(s)
        earliest_start = max(parent_end_times)# if len(parent_end_times) > 0 else 0
        if earliest_start > s or (Node.leftshift and earliest_start < s):
            s = earliest_start
            e = s + d
        self.start = s
        self.end = e

    def update_time_slot(self, du):
        s = self.start
        #d = e - s # determine real duration here
        d = du[self.operation][self.machine][self.worker]
        e = s + d#self.end
        parent_end_times = [parent.end + parent.buffer for parent in self.parents]
        parent_end_times.append(s)
        earliest_start = max(parent_end_times)# if len(parent_end_times) > 0 else 0
        if earliest_start > s or (Node.leftshift and earliest_start < s):
            s = earliest_start
            e = s + d
        self.start = s
        self.buffer = max(0, self.end+self.buffer - e)
        self.end = e
        
