from .Problem import Problem
from qiskit_optimization.applications import Maxcut
import matplotlib.pyplot as plt
from .utils import custom_colors
import networkx as nx
import json

class MaxcutProblem(Problem):
    def __init__(self, description):
        super().__init__(description)
        self.graph = description['graph']
        self.problem = Maxcut(self.graph)
        self.position = description['position']
        self.name = 'maxcut'
        self.n = len(self.graph.nodes())
        super().to_quadratic_program()
        super().to_qubo()
        super().solve()

    def visualize_problem(self, scaling_factor=1.0):
        # Setup plot with adjusted layout
        plt.figure(figsize=(16* scaling_factor, 12* scaling_factor))  # You can adjust the size to fit your needs
        colors = custom_colors['blue']['light']
        border_colors = custom_colors['blue']['dark']

        nodes = nx.draw_networkx_nodes(self.graph, self.position, node_color=colors, node_size=8000, edgecolors=border_colors, linewidths=10)
        # nodes = nx.draw_networkx_nodes(self.graph, self.position, node_color=colors, edgecolors=border_colors)
        nx.draw_networkx_edges(self.graph, self.position, width=8, edge_color=custom_colors['grey']['dark'])
        # nx.draw_networkx_edges(self.graph, self.position, edge_color=custom_colors['grey']['dark'])

        # nx.draw_networkx_labels(self.graph, self.position, font_weight='bold')
        nx.draw_networkx_labels(self.graph, self.position, font_weight='bold', font_size=48)
        is_weighted = any('weight' in data for _, _, data in self.graph.edges(data=True))
        if is_weighted:
            edge_labels = nx.get_edge_attributes(self.graph, 'weight')
            nx.draw_networkx_edge_labels(self.graph, self.position, edge_labels=edge_labels, font_size=48)
            # nx.draw_networkx_edge_labels(self.graph, self.position, edge_labels=edge_labels)

        plt.tight_layout()  # Apply tight layout to reduce padding
        return plt
        plt.show()

    def visualize_solution(self, solution = None, scaling_factor=1.0):
        if solution is None:
            solution = self.solution

        solution = solution[0]

        # Setup plot with adjusted layout
        plt.figure(figsize=(16 * scaling_factor, 12*scaling_factor))  # You can adjust the size to fit your needs
        print(solution)
        colors = [custom_colors['red']['light'] if solution[node] == 1 else custom_colors['green']['light'] for node in self.graph.nodes()]
        border_colors = [custom_colors['red']['dark'] if solution[node] == 1 else custom_colors['green']['dark'] for node in self.graph.nodes()]

        # nodes = nx.draw_networkx_nodes(self.graph, self.position, node_color=colors, node_size=8000, edgecolors=border_colors, linewidths=10)
        nodes = nx.draw_networkx_nodes(self.graph, self.position, node_color=colors, edgecolors=border_colors, node_size=8000, linewidths=10)
        # nx.draw_networkx_edges(self.graph, self.position, width=8, edge_color=custom_colors['grey']['dark'])
        nx.draw_networkx_edges(self.graph, self.position, edge_color=custom_colors['grey']['dark'], width=8)

        nx.draw_networkx_labels(self.graph, self.position, font_weight='bold', font_size=48)
        # nx.draw_networkx_labels(self.graph, self.position, font_weight='bold', font_size=48)
        is_weighted = any('weight' in data for _, _, data in self.graph.edges(data=True))
        if is_weighted:
            edge_labels = nx.get_edge_attributes(self.graph, 'weight')
            # nx.draw_networkx_edge_labels(self.graph, self.position, edge_labels=edge_labels, font_size=48)
            nx.draw_networkx_edge_labels(self.graph, self.position, edge_labels=edge_labels, font_size=48)

        

        plt.tight_layout()  # Apply tight layout to reduce padding
        # return plot to be able to save it
        return plt
        plt.show()

    def to_dict(self):
        # Convert the graph to a format that can be easily serialized
        graph_data = nx.node_link_data(self.graph)
        position_data = {node: [pos[0], pos[1]] for node, pos in self.position.items()}
        data = {
            'type': 'maxcut',
            'graph': graph_data,
            'position': position_data,
            'solution': self.solution
        }
        return data
