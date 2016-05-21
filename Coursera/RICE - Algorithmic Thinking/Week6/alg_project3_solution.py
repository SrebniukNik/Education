"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster
import random
import time
import pylab as plot
import alg_project3_viz
import alg_clusters_matplotlib
import re

######################################################
# Code for closest pairs of clusters


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.
    """
    cluster_s = []
    for cluster in cluster_list:
        if abs(cluster.horiz_center() - horiz_center) < half_width:
            cluster_s.append(cluster)
    cluster_s.sort(key=lambda c: c.vert_center())
    length = len(cluster_s)
    result = (float("inf"), -1, -1)
    for dummy_u in range(length - 1):
        for dummy_v in range(dummy_u + 1, min(dummy_u + 4, length)):
            idx1 = cluster_list.index(cluster_s[dummy_u])
            idx2 = cluster_list.index(cluster_s[dummy_v])
            check = pair_distance(cluster_list, idx1, idx2)
            #print dummy_u, 'result', check
            if check < result:
                result = check
        result = (result[0], min(result[1], result[2]), max(result[1], result[2]))
    return result


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    result = (float("inf"), -1, -1)
    #min_distance = float("inf")
    #cluster_list.sort(key=lambda cluster: cluster.horiz_center())
    length = len(cluster_list)
    for dummy_i in range(length):
        for dummy_j in range(dummy_i + 1, length):
            current_pair = pair_distance(cluster_list, dummy_i, dummy_j)
            if current_pair < result:
                result = current_pair
                #result = (min_distance, dummy_i, dummy_j)
    #print "slow", result
    return result


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    #cluster_list.sort(key=lambda cluster: cluster.horiz_center())
    length = len(cluster_list)
    if length <= 3:
        result = slow_closest_pair(cluster_list)
    else:
        middle = int(math.floor(0.5 * length))
        clist_left = cluster_list[0:middle]
        clist_right = cluster_list[middle:]
        result_left = fast_closest_pair(clist_left)
        right = fast_closest_pair(clist_right)
        result_right = (right[0], right[1]+middle, right[2]+middle)
        result = min(result_left, result_right)
        center_line = (cluster_list[middle - 1].horiz_center() + cluster_list[middle].horiz_center()) / 2
        closest = closest_pair_strip(cluster_list, center_line, result[0])
        result = min(result, closest)
    return result

# print fast_closest_pair([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 2, 0, 1, 0), alg_cluster.Cluster(set([]), 3, 0, 1, 0)])
#
# print fast_closest_pair([alg_cluster.Cluster(set([]), 0.38, 0.26, 1, 0), alg_cluster.Cluster(set([]), 0.42, 0.03, 1, 0), alg_cluster.Cluster(set([]), 0.48, 0.23, 1, 0), alg_cluster.Cluster(set([]), 0.8, 0.65, 1, 0), alg_cluster.Cluster(set([]), 0.95, 0.85, 1, 0), alg_cluster.Cluster(set([]), 0.97, 0.61, 1, 0)])
#expected one of the tuples in set([(0.10440306508900001, 0, 2)]) but received (0.20880613017821101, 1, 2)

#expected one of the tuples in set([(1.0, 1, 2), (1.0, 0, 1), (1.0, 2, 3)]) but received (inf, -1, -1)


######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    lenght = len(cluster_list)
    while lenght > num_clusters:
        cluster_list.sort(key=lambda cluster: cluster.horiz_center())
        closest = fast_closest_pair(cluster_list)
        cluster_to_merge = cluster_list[closest[2]]
        cluster_list[closest[1]].merge_clusters(cluster_to_merge)
        cluster_list.remove(cluster_to_merge)
        lenght -= 1
        print "Current cluster size", lenght

    return cluster_list


######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    cluster_lenght = len(cluster_list)
    cluster_pop = sorted(cluster_list, key=lambda cluster: cluster.total_population(), reverse=True)
    #print type(cluster_pop)
    cluster_pop = cluster_pop[:num_clusters]
    cluster_pop_lenght = len(cluster_pop)
    #print type(cluster_pop), len(cluster_pop)

    for dummy_n in range(num_iterations):
        cluster_final = [alg_cluster.Cluster(set([]), 0, 0, 0, 0) for dummy_i in range(num_clusters)]

        for cluster_orig in range(cluster_lenght):
            min_dist_idx = 0
            min_dist = float("inf")
            for dummy_k in range(cluster_pop_lenght):
                #print "lenght cluster list", cluster_lenght, cluster_orig, "dummy_k", dummy_k, "cluster_pop", cluster_pop
                distance = cluster_list[cluster_orig].distance(cluster_pop[dummy_k])
                if distance < min_dist:
                    min_dist = distance
                    min_dist_idx = dummy_k
            cluster_final[min_dist_idx].merge_clusters(cluster_list[cluster_orig])

        for num in range(cluster_pop_lenght):
            cluster_pop[num].merge_clusters(cluster_final[num])
    # position initial clusters at the location of clusters with largest populations

    return cluster_pop

# filename = 'unifiedCancerData_111.csv'
#
# def load_couties(filename):
#     inFile = open(filename, 'r')
#     lines = inFile.readlines()
#     cluster_list = [line.rstrip().split(',') for line in lines]
#     #print "cluster_list", cluster_list
#     return cluster_list
#
# clusters = load_couties(filename)
#
# cluster_list = [alg_cluster.Cluster(float(c[0]), float(c[1]), float(c[2]), float(c[3]), float(c[4])) for c in clusters]
#
# print "slow_closest_pair", slow_closest_pair(cluster_list)
#
# print "fast_closest_pair", fast_closest_pair(cluster_list)

# #print cluster_list
#
# print closest_pair_strip([alg_cluster.Cluster(set([]), 0, 0, 1, 0), alg_cluster.Cluster(set([]), 1, 0, 1, 0), alg_cluster.Cluster(set([]), 2, 0, 1, 0), alg_cluster.Cluster(set([]), 3, 0, 1, 0)], 1.5, 1.0)
#
# print closest_pair_strip([alg_cluster.Cluster(set([]), 0.02, 1.0, 1, 0), alg_cluster.Cluster(set([]), 0.02, 0.74, 1, 0), alg_cluster.Cluster(set([]), 0.1, 0.11, 1, 0), alg_cluster.Cluster(set([]), 0.44, 0.12, 1, 0), alg_cluster.Cluster(set([]), 0.61, 0.7, 1, 0)], 0.059999999999999998, 0.26000000000000001)
#
# print closest_pair_strip([alg_cluster.Cluster(set([]), 0.37, 0.28, 1, 0), alg_cluster.Cluster(set([]), 0.53, 0.24, 1, 0), alg_cluster.Cluster(set([]), 0.57, 0.32, 1, 0), alg_cluster.Cluster(set([]), 0.6, 0.42, 1, 0), alg_cluster.Cluster(set([]), 0.95, 0.85, 1, 0)], 0.55000000000000004, 0.104403)
#
# print closest_pair_strip([alg_cluster.Cluster(set([]), 0.11, 0.75, 1, 0), alg_cluster.Cluster(set([]), 0.62, 0.86, 1, 0), alg_cluster.Cluster(set([]), 0.65, 0.68, 1, 0), alg_cluster.Cluster(set([]), 0.68, 0.48, 1, 0), alg_cluster.Cluster(set([]), 0.7, 0.9, 1, 0), alg_cluster.Cluster(set([]), 0.79, 0.18, 1, 0)], 0.66500000000000004, 0.182482875909)
#
# print closest_pair_strip([alg_cluster.Cluster(set([]), -4.0, 0.0, 1, 0), alg_cluster.Cluster(set([]), 0.0, -1.0, 1, 0), alg_cluster.Cluster(set([]), 0.0, 1.0, 1, 0), alg_cluster.Cluster(set([]), 4.0, 0.0, 1, 0)], 0.0, 4.1231059999999999)
#expected one of the tuples in set([(0.26000000000000001, 0, 1)]) but received (0.63505905237229709, 1, 2)

#
# #print closest_pair_strip(cluster_1)
#

def gen_random_clusters(num_clusters):
    '''
    Func for random cluster list generation
    :param num_clusters:
    :return: list of cluster
    '''
    cluster_list = []
    for num in range(num_clusters):
        x_coord = round(random.random(), 2)
        y_coord = round(random.random(), 2)
        cluster = alg_cluster.Cluster(set([num]), x_coord, y_coord, 1, 0.01)
        cluster_list.append(cluster)
    return cluster_list


def question1(num_clusters, file_to_save):
    '''
    Func for plotting time execution of 2 algorithms
    :param iterations: integer
    :param num_clusters: integer
    :return: plot
    '''
    slow_time = []
    fast_time = []

    for num in range(2, num_clusters):
        cluster_list = gen_random_clusters(num)
        cluster_list.sort(key=lambda cluster: cluster.horiz_center())
        start_time = time.time()
        slow_closest_pair(cluster_list)
        stop_time = time.time()
        slow_time.append(abs(stop_time - start_time))
        start_time = time.time()
        fast_closest_pair(cluster_list)
        stop_time = time.time()
        fast_time.append(abs(stop_time - start_time))

        print slow_time
    print fast_time
    plot.plot(range(2, num_clusters), slow_time, '-r', label='Slow cluster algorithm')
    plot.plot(range(2, num_clusters), fast_time, '-g', label='Fast cluster algorithm')

    plot.title('Slow vs fast clustering algorithm - PyCharm (IntelliJ)')
    plot.xlabel('Size of Cluster')
    plot.ylabel('Running time in seconds')
    plot.legend(loc='upper right')
    # plot.tight_layout()
    if file_to_save:
        plot.savefig(file_to_save)


def question2(URL, file_to_save, number_clusters=15, centers=False):
    '''

    :return:
    '''
    data_table, singleton_list = alg_project3_viz.run_example(URL)
    cluster_list = hierarchical_clustering(singleton_list, number_clusters)
    print "Displaying", len(cluster_list), "hierarchical clusters"
    if centers:
        file = file_to_save[:-4] + 'with_centers' + '.png'
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, file, centers)
    alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, file_to_save, centers)


def question3(URL, file_to_save, number_clusters=15, iterations=5, centers=False):
    '''

    :return:
    '''
    data_table, singleton_list = alg_project3_viz.run_example(URL)
    cluster_list = kmeans_clustering(singleton_list, number_clusters, iterations)
    print "Displaying", len(cluster_list), "k-means clusters"
    if centers:
        file = file_to_save[:-4] + 'with_centers' + '.png'
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, file, centers)
    alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, file_to_save, centers)

def question5(URL, file_to_save, number_clusters=9, centers=False):
    '''

    :return:
    '''
    data_table, singleton_list = alg_project3_viz.run_example(URL)
    cluster_list = hierarchical_clustering(singleton_list, number_clusters)
    print "Displaying", len(cluster_list), "hierarchical clusters"
    if centers:
        file = file_to_save[:-4] + 'with_centers' + '.png'
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, file, True)
    alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, file_to_save, False)


def question6(URL, file_to_save, number_clusters=9, iterations=5, centers=False):
    '''

    :return:
    '''
    data_table, singleton_list = alg_project3_viz.run_example(URL)
    cluster_list = kmeans_clustering(singleton_list, number_clusters, iterations)
    print "Displaying", len(cluster_list), "k-means clusters"
    if centers:
        file = file_to_save[:-4] + 'with_centers' + '.png'
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, file, True)
    alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, file_to_save, False)


def question7(URL, number_clusters=9, iterations=5):
    '''

    :return:
    '''
    data_table, singleton_list = alg_project3_viz.run_example(URL)
    cluster_list_hierarchical = hierarchical_clustering(singleton_list, number_clusters)
    cluster_list_kmeans = kmeans_clustering(singleton_list, number_clusters, iterations)
    hierarchical_distortion = sum([x.cluster_error(data_table) for x in cluster_list_hierarchical])
    kmeans_distortion = sum([y.cluster_error(data_table) for y in cluster_list_kmeans])
    counties = re.search('_(\d+)\.csv', URL).group(1)
    print "Displaying distortion of hierarchical clusteringfor", counties, "counties", hierarchical_distortion
    print "Displaying distortion of k-means clustering", counties, "counties", kmeans_distortion

def question10(URLs, min_number_clusters=6, max_number_clusters=20, steps=5, file_to_save="Question10.png"):
    '''

    :return:
    '''
    for url in URLs:
        hierarchical_distortion_result = []
        kmeans_distortion_result = []
        for num in range(max_number_clusters,min_number_clusters-1,-1):
            data_table, singleton_list = alg_project3_viz.run_example(url)
            cluster_list_hierarchical = hierarchical_clustering(singleton_list, num)
            hierarchical_distortion = sum([x.cluster_error(data_table) for x in cluster_list_hierarchical])
            hierarchical_distortion_result.append(hierarchical_distortion)
        hierarchical_distortion_result.reverse()

        for num in range(min_number_clusters, max_number_clusters + 1):
            data_table, singleton_list = alg_project3_viz.run_example(url)
            #print "num clsusters", num
            cluster_list_kmeans = kmeans_clustering(singleton_list, num, steps)
            kmeans_distortion = sum(cluster.cluster_error(data_table) for cluster in cluster_list_kmeans)
            #print "kmeans distortion", kmeans_distortion
            kmeans_distortion_result.append(kmeans_distortion)

        counties = re.search('_(\d+)\.csv', url).group(1)
        print "hierarchical clustering with", num, "cluster for", counties, "counties", hierarchical_distortion_result
        print "k-means clustering with", num, "cluster for", counties, "counties", kmeans_distortion_result, "\n"

        label_hierar = 'Distortion of hierarchical clustering for' + counties
        label_kmeans = 'Distortion of k-means clustering for' + counties
        range0 = range(min_number_clusters, max_number_clusters+1)

        plot.plot(range0, hierarchical_distortion_result, '-r', label=label_hierar)
        plot.plot(range0, kmeans_distortion_result, '-g', label=label_kmeans)

        plot.title('Hierarchical vs K-means distortion - PyCharm (IntelliJ)')
        plot.xlabel('Size of Cluster')
        plot.ylabel('Distortion')
        plot.legend(loc='upper right')
        plot.tight_layout()
        if file_to_save:
            file = file_to_save[:-4] + "_" + counties + '.png'
            plot.savefig(file)
        plot.clf()


def main():
    '''

    :return:
    '''
    ####Question1####
    #question1(200, "question1.png")

    ####Question2####
    #question2(alg_project3_viz.DATA_896_URL, "Question2.png", 15, False)

    ####Question3####
    #question3(alg_project3_viz.DATA_896_URL, "Question3.png", 15, 5, False)

    ###Question 4.
    #K-means clustering is faster because the running time is O(n2log2n), therefore running time of
    #k-means clustering is O(n)

    ####Question5####
    #question5(alg_project3_viz.DATA_111_URL, "Question5.png", 9, True)

    ####Question6####
    #question6(alg_project3_viz.DATA_111_URL, "Question6.png", 9, 5, True)

    ####Question7####
    # Displaying distortion of hierarchical clusteringfor 111 counties 1.75163886916e+11
    # Displaying distortion of k-means clustering 111 counties 1.75163886916e+11
    #question7(alg_project3_viz.DATA_111_URL, 9, 5)


    ####Question 8####
    # On west coast clusters look like similar.
    # In k-means clustering 3 clusters are located in California, when in hierarchical - only 2.
    #

    ####Question 9####
    #Hierarchical clustering requires less human supervision to produce clustering with relatively low distortion.

    ####Question 10
    #URLs = [alg_project3_viz.DATA_111_URL, alg_project3_viz.DATA_290_URL, alg_project3_viz.DATA_896_URL]
    URLs = [alg_project3_viz.DATA_290_URL, alg_project3_viz.DATA_896_URL]
    #URLs = [alg_project3_viz.DATA_111_URL]
    question10(URLs, 6, 20, 5, "Question10.png")

    ####Question11####
    ####No one method produces lower distortion clustering.


if __name__ == '__main__':
    main()