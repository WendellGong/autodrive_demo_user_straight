import matplotlib.pyplot as plt

def is_point_between_curves(point, curve1, curve2):
    x, y = point['x'], point['y']
    for i in range(len(curve1)):
        if curve1[i]['y'] <= y <= curve2[i]['y']:
            return True
    return False

def visualize_curves_and_point(curve1, curve2, point):
    # Extract x and y values for curves
    x_curve1 = [point['x'] for point in curve1]
    y_curve1 = [point['y'] for point in curve1]

    x_curve2 = [point['x'] for point in curve2]
    y_curve2 = [point['y'] for point in curve2]

    # Extract x and y values for the point
    x_point = point['x']
    y_point = point['y']

    # Plot the curves
    plt.figure(figsize=(8, 6))
    plt.plot(x_curve1, y_curve1, label='Curve 1', color='blue')
    plt.plot(x_curve2, y_curve2, label='Curve 2', color='green')

    # Plot the point
    plt.scatter(x_point, y_point, color='red', label='Point')

    # Check if the point is between curves
    if is_point_between_curves(point, curve1, curve2):
        plt.title('Visualization - Point is Between Curves')
    else:
        plt.title('Visualization - Point is Not Between Curves')

    # Add labels and legend
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()

    # Show plot
    plt.grid(True)
    plt.show()

# Example curves
curve1 = [{'x': 7.5, 'y': 76.09}, {'x': 7.5, 'y': 65.22}, {'x': 7.5, 'y': 54.35}, {'x': 7.5, 'y': 43.48}, {'x': 7.5, 'y': 32.61}, {'x': 7.5, 'y': 21.74}, {'x': 7.5, 'y': 10.87}, {'x': 7.5, 'y': 0.0}, {'x': 7.49, 'y': -10.87}, {'x': 7.49, 'y': -21.74}, {'x': 7.49, 'y': -32.61}, {'x': 7.49, 'y': -43.48}, {'x': 7.49, 'y': -54.35}, {'x': 7.49, 'y': -65.22}, {'x': 7.49, 'y': -76.09}, {'x': 7.49, 'y': -86.96}, {'x': 7.49, 'y': -97.83}, {'x': 7.49, 'y': -108.7}]

curve2 = [{'x': 3.76, 'y': 76.09}, {'x': 3.76, 'y': 65.22}, {'x': 3.76, 'y': 54.35}, {'x': 3.76, 'y': 43.48}, {'x': 3.76, 'y': 32.61}, {'x': 3.76, 'y': 21.74}, {'x': 3.76, 'y': 10.87}, {'x': 3.76, 'y': 0.0}, {'x': 3.75, 'y': -10.87}, {'x': 3.75, 'y': -21.74}, {'x': 3.75, 'y': -32.61}, {'x': 3.75, 'y': -43.48}, {'x': 3.75, 'y': -54.35}, {'x': 3.75, 'y': -65.22}, {'x': 3.75, 'y': -76.09}, {'x': 3.75, 'y': -86.96}, {'x': 3.75, 'y': -97.83}, {'x': 3.75, 'y': -108.7}]

# Example point
point = {'x': 15, 'y': 0}

# Visualize curves and point
visualize_curves_and_point(curve1, curve2, point)
if is_point_between_curves(point,curve1,curve2):
    print("yes")