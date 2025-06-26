import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Create the matplotlib figure and canvas
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)

    def update_chart(self, years, portfolio_values):
        # Clear the previous chart
        self.figure.clear()
        
        # Create the bar chart
        ax = self.figure.add_subplot(111)
        ax.bar(years, portfolio_values)
        
        # Customize the chart
        ax.set_xlabel('Year')
        ax.set_ylabel('Portfolio Value')
        ax.set_title('Retirement Portfolio Projection')
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Adjust layout and redraw
        self.figure.tight_layout()
        self.canvas.draw()

# Example usage (for testing purposes)
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    results_panel = ResultsPanel()
    results_panel.show()
    
    # Simulate data and update chart
    import numpy as np
    years = np.arange(2023, 2053)
    portfolio_values = np.random.randint(100000, 1000000, size=30)
    results_panel.update_chart(years, portfolio_values)
    
    sys.exit(app.exec_())
