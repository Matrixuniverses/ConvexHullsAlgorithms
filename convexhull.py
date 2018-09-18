"""
   Author: Matrixuniverses
"""


import time


def readDataPts(filename, N):
    """ Reads the first N lines of data from the input file
        and returns a list of N tuples
        [(x0,y0), (x1, y1), ...]
    """
    
    # Creates a list with N points
    try:
        source_file_raw = open(filename)
        source_lines = source_file_raw.read().splitlines()
        listPts = []
    
        for line_num in range(N):
            point = source_lines[line_num].split()
            point_formatted = (float(point[0]), float(point[1]))
            listPts.append(point_formatted)

        source_file_raw.close()

    # Catches a file not found error and exits program
    except FileNotFoundError as e:
        print('{0}\n Exiting...'.format(e))
        exit(1)

    return listPts


def theta(point_1, point_2):
    """ Taanchor_indexes two points and calculates the approximate angle 
        between them and the pervious incident line
    """

    dx = point_2[0] - point_1[0]
    dy = point_2[1] - point_1[1]
    
    # Catching if the points are co-linear to prevent db0 error
    if abs(dx) < 1e-9 and abs(dy) < 1e-9:
        t = 0
    else:
        t = dy / (abs(dx) + abs(dy))
  
    # If points are equal their angle is 0 not 360
    if point_1 == point_2:
        return 0

    # If dx is negative, 90 < theta < 270
    if dx < 0:
        t = 2 - t
    
    # If dy is negative 180 < theta < 360
    elif dy < 0:
        t = 4 + t

    # If t is 0, it is the same as being 360 degrees
    elif t == 0:
        return 360

    # Converting the t values into degree values
    return t * 90


def min_y(listPts):
    """ Returns a tuple of the minimum-rightmost point 
        of the given point list
    """

    # Defining the initial minimum values
    min_y = float('inf')
    min_point = None

    # Iteration through all points to find all those with lowest y co-ordinate 
    for point in listPts:
        if point[1] < min_y:

            # Found a new min point
            min_y = point[1]
            min_point = point

        # Found a point on the same y level as the min point
        elif point[1] == min_y:

            # Choosing the right most point off of x value
            if point[0] > min_point[0]:
                min_point = point

    return min_point, listPts.index(min_point)


def isCCW(point_a, point_b, point_c):
    """ Returns true if the supplied points are counter-clockwise
    """
   
    # Returns a boolean value for checking if 3 points are counter-clockwise
    return ((point_b[0] - point_a[0]) * (point_c[1] - point_a[1]) - 
            (point_b[1] - point_a[1]) * (point_c[0] - point_a[0])) > 0 


def giftwrap(listPts):
    """ Returns the convex hull vertices computed using the
        giftwrap algorithm as a list of m tuples
        [(u0,v0), (u1,v1), ...]    
    """

    # Defining the anchor point and its index
    anchor, anchor_index = min_y(listPts)
    listPts.append(anchor)

    # Set up variables for the gift wrap algoritm
    index, prev_angle = 0, 0
    convex_hull = []

    while anchor_index != len(listPts) - 1:
        # Swapping points through parallel assignment 
        listPts[index], listPts[anchor_index] = listPts[anchor_index], listPts[index]

        # Resetting start state variables for each vertex
        min_angle = 361
        convex_hull.append(listPts[index])
        
        # Iterating over the remaining unscanned points
        for i in range(index + 1, len(listPts)):
            angle = theta(listPts[index], listPts[i])

            # Finding the next convex hull point that is different from the previous one
            if angle < min_angle and angle > prev_angle and listPts[index] != listPts[i]:
                min_angle = angle
                anchor_index = i

        # Go to next point in point set
        index += 1
        prev_angle = min_angle
    
    return convex_hull


def grahamscan(listPts):
    """ Returns the convex hull vertices computed using the
        Graham-scan algorithm as a list of m tuples
        [(u0,v0), (u1,v1), ...]  
    """

    # Defining the starting point and initialize an empty list to hold the points
    anchor, anchor_index = min_y(listPts)
    theta_sorted = []

    # Adding all points to the new point list in format: (angle in degs, point)
    for i in range(len(listPts)):
        angle = (theta(anchor, listPts[i]), listPts[i])
        theta_sorted.append(angle)

    # Sorts the point list by angle
    theta_sorted = sorted(theta_sorted, key = lambda x: x[0])
    theta_sorted = [x[1] for x in theta_sorted]
   
    # Defines stack
    stack = theta_sorted[:3]
    
    # Performs the graham scan algorithm
    for i in range(3, len(theta_sorted)):
        while not isCCW(stack[-2], stack[-1], theta_sorted[i]):
            stack.pop()
        stack.append(theta_sorted[i])
                
    return stack


def amethod(listPts):
    """ Returns the convex hull vertices computed using 
        the monochain algorithm
    """
    
    # Initializing variables for the upper and lower hulls
    upper_hull, lower_hull = [], []
    
    # Sorting the points by x co-ordinate
    x_sorted = sorted(listPts, key = lambda x: x[0])

    # Performing the upper iteration of the algorithm
    for point in x_sorted:
        while len(lower_hull) >= 2 and not isCCW(lower_hull[-2], lower_hull[-1], point):
            lower_hull.pop()
        lower_hull.append(point)
    
    # Performing the lower iteration of the algorithm
    for point in reversed(x_sorted):
        while len(upper_hull) >= 2 and not isCCW(upper_hull[-2], upper_hull[-1], point):
            upper_hull.pop()
        upper_hull.append(point)

    # Returning the upper and lower hull concatonated together, minus the final point 
    # as it is a duplication
    return lower_hull[:-1] + upper_hull[:-1]


def main():
    """ Prints the convex hulls of the given dataset, this method is not generally 
        used as the testing suite will call the required methods
    """

    #print('Giftwrap: ' + giftwrap(readDataPts('A_3000.dat', 3000)))
    #print('Grahamscan: ' + grahamscan(readDataPts('A_6000.dat', 6000)))
    #print('Monotone chain: {0}'.format(amethod(readDataPts('Sets/A_3000.dat', 3000))))

    amethod(readDataPts('Sets/A_3000.dat', 3000))


if __name__ == "__main__":
    main()
