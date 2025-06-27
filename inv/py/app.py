def calculate_area(rect):
    """Calculates the area of a rectangle given its coordinates."""
    x1, y1, x2, y2 = rect
    return abs(x2 - x1) * abs(y2 - y1)

rectangles = [
    (0, 0, 2, 3),  # Rectangle 1
    (1, 1, 3, 4),  # Rectangle 2
    (2, 2, 4, 5)   # Rectangle 3
]

# Sort the rectangles by their area
sorted_rectangles = sorted(rectangles, key=calculate_area)

print(sorted_rectangles)