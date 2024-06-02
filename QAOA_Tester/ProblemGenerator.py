from .Problem import Problem
from .KnapsackProblem import KnapsackProblem 
from .MaxcutProblem import MaxcutProblem
from .utils import custom_colors
import random
import networkx as nx
import numpy as np
import math 


class ProblemGenerator:
    def __init__(self):
        self.problem = None

    def generate_knapsack(self, n: int, weight_range: tuple , profit_range: tuple, profit_as_weight=False):
        description = self._generate_knapsack_items(n, weight_range, profit_range, profit_as_weight)
        self.problem = KnapsackProblem(description= description)
        return self.problem

    def _generate_knapsack_items(self, n: int, weight_range: tuple , profit_range: tuple, profit_as_weight=False):
        # Generate items with random weights and profits
        min_weight, max_weight = weight_range
        min_profit, max_profit = profit_range

        weights = [random.randint(min_weight, max_weight) for _ in range(n)]
        if profit_as_weight:
            profits = weights
        else:
            profits = [random.randint(min_profit, max_profit) for _ in range(n)]
        
        # Calculate a constraint that's half the sum of the weights but an integer
        constraint = math.ceil(sum(weights) / 2)
        
        # Assign a random color to each item from matplotlib's TABLEAU_COLORS
        # colors = list(mcolors.TABLEAU_COLORS.keys())
        colors = list(custom_colors.keys())
        if n > len(colors):
            # add the same colors again if we need more than the default colors
            colors = colors * (n // len(colors) + 1)
        random.shuffle(colors)  # Shuffle colors to ensure randomness

        # Return the problem as a dictionary of items and constraint
        items = []
        for i in range(n):
            items.append({
                'weight': weights[i],
                'profit': profits[i],
                'color': colors[i]
            })

        description = {
            'items': items,
            'constraint': constraint
        }

        return description

    def generate_maxcut(self, num_nodes: int, num_edges: int, weights=False):
        graph = self._generate_maxcut_graph(num_nodes, num_edges, weights= weights)
        position = nx.spring_layout(graph)
        description = {
            'graph': graph,
            'position': position
        }
        self.problem = MaxcutProblem(description=description)
        return self.problem

    def _generate_maxcut_graph(self, n_nodes, n_edges, weight_range=(1, 10), weights=False):
        # Generate a random graph with n_nodes and n_edges
        G = nx.gnm_random_graph(n_nodes, n_edges)
        min_weight, max_weight = weight_range

        # Assign random weights to the edges
        G.add_weighted_edges_from([(u, v, np.random.randint(min_weight, max_weight)) for u, v in G.edges()])


        return G

    def from_dict(data):
        if data['type'] == 'knapsack':
            description = {
                'items': data['items'],
                'constraint': data['constraint']
            }
            problem = KnapsackProblem(description)

        elif data['type'] == 'maxcut':
            description = {
                'graph': nx.node_link_graph(data['graph']),
                'position': data['position']
            }
            problem = MaxcutProblem(description)

        return problem