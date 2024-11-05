import numpy as np
import matplotlib.pyplot as plt

# Function to display letters "О" and "Л" as matrices
def display_letter_as_matrix(letter):
    if letter == 'О':
        # Matrix for letter "О"
        matrix = np.array([[1, 1, 1, 1, 1],
                           [1, 0, 0, 0, 1],
                           [1, 0, 0, 0, 1],
                           [1, 0, 0, 0, 1],
                           [1, 1, 1, 1, 1]])
    elif letter == 'Л':
        # Matrix for letter "Л"
        matrix = np.array([[0, 1, 1, 1, 0],
                           [0, 1, 0, 1, 0],
                           [0, 1, 0, 1, 0],
                           [0, 1, 0, 1, 0],
                           [1, 1, 0, 1, 0]])
    
    plt.imshow(matrix, cmap='Greys', interpolation='nearest')
    plt.axis('off')
    plt.title(f'Буква: {letter}')
    plt.show()