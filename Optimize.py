from Pattern import Pattern
import numpy as np
import itertools

class Optimize():
    '''Implements functions to detect and Optimize Point distances of points in diffrent patterns'''
    def __init__(self, pattern):
        self.pattern = pattern

    def flag_point_dist(self):
        lists_of_points = [
            np.array([(1, 0), (10, 12), (5, 5)]),
            np.array([(2, 3), (20, 30), (0, 0)]),
            np.array([(100, 100), (4, 4)]),
            np.array([(-1, -1), (50, 50)])
        ]

        if len(lists_of_points) < 2:
            return

        global_min_dist = float('inf')
        best_pair = None
        best_list_indices = None

        # Iterate through every unique pair of lists
        for idx1, idx2 in itertools.combinations(range(len(lists_of_points)), 2):
            l1 = lists_of_points[idx1]
            l2 = lists_of_points[idx2]
            
            # Your broadcasted pairwise calculation
            distances = np.linalg.norm(l1[:, np.newaxis] - l2, axis=2)
            
            # Find the minimum in this specific pair of lists
            current_min = np.min(distances)
            
            if current_min < global_min_dist:
                global_min_dist = current_min
                
                # Track exactly which points and lists they came from
                min_idx = np.unravel_index(np.argmin(distances), distances.shape)
                best_pair = (l1[min_idx[0]], l2[min_idx[1]])
                best_list_indices = (idx1, idx2)

        print(f"Shortest Distance: {global_min_dist}")
        print(f"Between point {best_pair[0]} (List {best_list_indices[0]}) and point {best_pair[1]} (List {best_list_indices[1]})")

if __name__ == '__main__':
    o = Optimize(None)
    o.flag_point_dist()
