from Problem import Problem
from qiskit_optimization.applications import Knapsack
import matplotlib.pyplot as plt
import numpy as np
from utils import custom_colors

class KnapsackProblem(Problem):
    def __init__(self, description):
        super().__init__(description)
        self.n = len(description['items'])
        self.items = description['items']
        self.constraint = description['constraint']

        # store the values, weights, and colors separately for easier access
        self.values = [item['profit'] for item in description['items']]
        self.weights = [item['weight'] for item in description['items']]
        self.colors = [item['color'] for item in description['items']]
        self.problem = Knapsack(values = self.values, weights = self.weights, max_weight = self.constraint)

        super().to_quadratic_program()
        super().to_qubo()
        super().solve()

    def visualize_problem(self):
        # Convert to numpy arrays for element-wise operations
        weights = np.array(self.weights)
        values = np.array(self.values)
       
        seperator = 0.5

        # Normalize profit values to a suitable range for bar widths, ensuring visibility
        value_widths = values / weights
        
        # Create figure and axes for the plot
        fig, ax = plt.subplots()

        # Set initial x position
        x_pos = 0
        label_pos = []
        # Plot each item as a separate bar on the x-axis
        for i, (weight, value_width, color) in enumerate(zip(weights, value_widths, self.colors)):
            ax.bar(x_pos + 0.5* value_width, weight, width=value_width, color=custom_colors[color]['light'] , edgecolor=custom_colors[color]['dark'])
            label_pos.append(x_pos + 0.5*value_width)
            x_pos += value_width + seperator # Move x position for the next bar
                
            # Add labels for the values on top of the bars
            ax.text(label_pos[-1], weight / 2, str(values[i]),
                        ha='center', va='center', color='black')
                

        # Add a constraint line to visualize the weight limit
        ax.axhline(self.constraint, color='r', linestyle='--')

        ax.set_xlabel('Item')
        ax.set_ylabel('Weight $w_i$')
        ax.set_title('Knapsack Problem (Item area is proportional to its value $v_i$)')

        # Set x-ticks to be visible for each bar
        ax.set_xticks(label_pos)
        ax.set_xticklabels([f'Item {i+1}' for i in range(self.n)])

        # add a legend for the constraint line
        ax.legend(['Weight Constraint $W$'], loc='upper right')

        plt.show()


    def visualize_solution(self, solution=None):
         # Default to selecting all items if no solution is provided
        if solution is None:
            solution = self.solution
        else:
            # ensure the solution is only the first n elements
            solution = (solution[0][:self.n], solution[1])
        
        # Convert to numpy arrays for element-wise operations
        weights = np.array(self.weights)
        profits = np.array(self.values)
        solution = np.array(solution[0])

        # Apply the solution to select items
        selected_weights = weights * solution
        selected_profits = profits * solution

        # Normalize profit values to a suitable range for bar widths, ensuring visibility
        profit_widths = selected_profits

        # Compute the cumulative sum for stacking
        cumulative_weights = np.cumsum(selected_weights[::-1])[::-1]

        # Create figure and axes for the plot
        fig, ax = plt.subplots()

        # Initial bar's x position and base width
        x_pos = 0
        base_width = 0  # Base width to ensure even small profit items are visible

        # Plot each selected item as a segment of the stacked bar, adjusting width by profit
        bottom = 0
        for weight, profit_width, color in zip(selected_weights, profit_widths, self.colors):
            if weight > 0:  # Only plot selected items
                ax.bar(x_pos, weight, bottom=bottom, color=custom_colors[color]['light'] , width=base_width + profit_width, align='edge', edgecolor=custom_colors[color]['dark'], linewidth=2)
                bottom += weight

        # Add a constraint line to visualize the limit
        ax.axhline(self.constraint, color='r', linestyle='--')

        ax.set_xlabel('Value')
        ax.set_ylabel('Weight')
        # ax.set_title('Knapsack Problem Solution with Profit-Adjusted Width')

        # Return the figure and axes instead of showing it
        plt.show()


        

if __name__ == "__main__":
    problem = KnapsackProblem({
        'items': [
            {'weight': 19, 'profit': 58, 'color': 'green'},
            {'weight': 11, 'profit': 56, 'color': 'blue'},
            {'weight': 16, 'profit': 42, 'color': 'orange'},
            {'weight': 11, 'profit': 41, 'color': 'yellow'},
            {'weight': 19, 'profit': 15, 'color': 'red'}
        ],
        'constraint': 38
    })
    problem.visualize_problem()
