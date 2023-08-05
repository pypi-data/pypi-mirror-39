import numpy as np
from mag.np.arr import runs, binarize, nonzero_1d, consecutive

from scipy.spatial.distance import euclidean
from numpy import mean, subtract

def iou_1d(predicted_boundary, target_boundary):
    '''Calculates the intersection over union (IOU) based on a span.

    Notes:
        boundaries are provided in the the form of [start, stop].
        boundaries where start = stop are accepted
        boundaries are assumed to be only in range [0, int < inf)

    Args:
        predicted_boundary (list): the [start, stop] of the predicted boundary
        target_boundary (list): the ground truth [start, stop] for which to compare

    Returns:
        iou (float): the IOU bounded in [0, 1]
    '''

    p_lower, p_upper = predicted_boundary
    t_lower, t_upper = target_boundary

    # boundaries are in form [start, stop] and 0 <= start <= stop
    assert 0<= p_lower <= p_upper
    assert 0<= t_lower <= t_upper

    # no overlap, pred is too far left or pred is too far right
    if p_upper < t_lower or p_lower > t_upper:
        return 0

    if predicted_boundary == target_boundary:
        return 1

    intersection_lower_bound = max(p_lower, t_lower)
    intersection_upper_bound = min(p_upper, t_upper)

    intersection = intersection_upper_bound - intersection_lower_bound

    max_upper = max(t_upper, p_upper)
    min_lower = min(t_lower, p_lower)

    union = max_upper - min_lower

    union = union if union != 0 else 1
    return min(intersection / union, 1)


def detect_channel_binary_objects(channel:list):
    channel = np.array(channel)
    signal_indicies = nonzero_1d(channel)
    if signal_indicies.size == 0:
        return []
    consec_indicies = consecutive(signal_indicies, stepsize=1)
    return runs(signal_indicies)


def detect_sequence_binary_objects(channel_matrix, cutoff:float=0.5):
    channel_matrix = binarize(np.array(channel_matrix), cutoff)
    return [detect_channel_binary_objects(channel) for channel in channel_matrix]


def process_1d(output_channel_matrix, target_channel_matrix, cutoff=0.5):
    metrics = {}

    metrics['perfect_absence'] = 0
    metrics['perfect_coverage'] = 0
    metrics['total_output_objects'] = 0
    metrics['total_target_objects'] = 0
    metrics['total_false_positives'] = 0
    metrics['total_false_negatives'] = 0
    metrics['all_offsets'] = []
    metrics['total_average_offset'] = []


    output_channel_matrix = binarize(np.array(output_channel_matrix), cutoff)
    target_channel_matrix = np.array(target_channel_matrix)

    output_channel_objects = target_channel_objects = []
    output_channel_offsets = target_channel_offsets = []

    for channel_index in range(len(target_channel_matrix)):
        # shorter
        channel_str = 'channel_{}_'.format(channel_index)

        # current channel
        output_channel = output_channel_matrix[channel_index]
        target_channel = target_channel_matrix[channel_index]

        # get objects
        output_objects = detect_channel_binary_objects(output_channel)
        target_objects = detect_channel_binary_objects(target_channel)

        # save some computation
        n_output_objects = len(output_objects)
        n_target_objects = len(target_objects)

        # update totals
        metrics['total_output_objects'] += n_output_objects
        metrics['total_target_objects'] += n_target_objects

        # keep track of total
        metrics[channel_str+'number_of_output_objects'] = n_output_objects
        metrics[channel_str+'number_of_target_objects'] = n_target_objects

        metrics[channel_str+'output_objects'] = output_objects
        metrics[channel_str+'target_objects'] = target_objects

        # channel's fp / fn rates
        metrics[channel_str+'false_positives'] = 0
        metrics[channel_str+'false_negatives'] = 0

        # channel's tp rate
        metrics[channel_str+'perfect_absence'] = 0
        metrics[channel_str+'perfect_coverage'] = 0

        metrics[channel_str+'offsets'] = []
        metrics[channel_str+'average_offset'] = []

        # store objects
        # output_channel_objects.append(output_objects)
        # target_channel_objects.append(target_objects)

        if n_output_objects == n_target_objects == 0:
            # no objects in either
            metrics['perfect_absence'] += 1
            metrics[channel_str+'perfect_absence'] += 1

        elif n_output_objects == 0:
            # false negative: target_objects(s) but no output_object
            metrics['total_false_negatives'] += n_target_objects
            metrics[channel_str+'false_negatives'] += n_target_objects

        elif len(target_objects) == 0:
            # false positive: output_object(s) but no target_objects
            metrics['total_false_positives'] += n_output_objects
            metrics[channel_str+'false_positives'] += n_output_objects

        else:
            # align
            offsets = []

            for outobj in output_objects:
                pairwise_ious = [iou_1d(outobj, tarobj) for tarobj in target_objects]
                pairwise_eucl = [euclidean(outobj, tarobj) for tarobj in target_objects]

                alignment_scores = pairwise_eucl if not any(pairwise_ious) else pairwise_ious

                num_perfect = np.where(np.array(pairwise_ious) == 1)[0].size
                metrics['perfect_coverage'] += num_perfect
                metrics[channel_str+'perfect_coverage'] += num_perfect

                closest = alignment_scores.index(min(alignment_scores))
                aligned = target_objects[closest]
                offset = subtract(outobj, aligned)
                offsets.append(offset)

            average_offset = [mean(errors) for errors in zip(*offsets)]
            metrics['all_offsets'] += offsets
            metrics[channel_str+'offsets'] = offsets
            metrics[channel_str+'average_offset'] = average_offset

        metrics['total_average_offset'] = [mean(error) for error in zip(*metrics['all_offsets'])]

    return metrics



import os
from multiprocessing import Pool
def batch_process_1d(batched_output_channel_matrix, batched_target_channel_matrix, cutoff=0.5, processes:int=None):
    merged = {}

    if processes is None: processess = os.cpu_count()

    pool = Pool(processes=processess)

    starargs = [
        (
            batched_output_channel_matrix[example_index],
            batched_target_channel_matrix[example_index],
            cutoff
        ) for example_index in range(len(batched_target_channel_matrix))
    ]

    metrics = pool.starmap(process_1d, starargs)

    return metrics

def merge_batched_metrics(mapped_metrics:dict, num_channels:int):
    merged = {}
    merged['perfect_absence'] = 0
    merged['perfect_coverage'] = 0
    merged['total_output_objects'] = 0
    merged['total_target_objects'] = 0
    merged['total_false_positives'] = 0
    merged['total_false_negatives'] = 0
    merged['all_offsets'] = []
    merged['total_average_offset'] = []

    for channel_index in range(num_channels):
        channel_str = 'channel_{}_'.format(channel_index)
        merged[channel_str+'output_objects'] = []
        merged[channel_str+'target_objects'] = []
        merged[channel_str+'offsets'] = []

        merged[channel_str+'number_of_output_objects'] = 0
        merged[channel_str+'number_of_target_objects'] = 0
        merged[channel_str+'false_positives'] = 0
        merged[channel_str+'false_negatives'] = 0
        merged[channel_str+'perfect_absence'] = 0
        merged[channel_str+'perfect_coverage'] = 0

    for metrics in mapped_metrics:
        merged['perfect_absence'] += metrics['perfect_absence']
        merged['perfect_coverage'] += metrics['perfect_coverage']
        merged['total_output_objects'] += metrics['total_output_objects']
        merged['total_target_objects'] += metrics['total_target_objects']
        merged['total_false_positives'] += metrics['total_false_positives']
        merged['total_false_negatives'] += metrics['total_false_negatives']

        merged['all_offsets'] += metrics['all_offsets']
        # merged['total_average_offset'] += metrics['total_average_offset']

        for channel_index in range(num_channels):
            channel_str = 'channel_{}_'.format(channel_index)
            merged[channel_str+'output_objects'] += metrics[channel_str+'output_objects']
            merged[channel_str+'target_objects'] += metrics[channel_str+'target_objects']
            merged[channel_str+'false_positives'] += metrics[channel_str+'false_positives']
            merged[channel_str+'false_negatives'] += metrics[channel_str+'false_negatives']
            merged[channel_str+'perfect_absence'] += metrics[channel_str+'perfect_absence']
            merged[channel_str+'perfect_coverage'] += metrics[channel_str+'perfect_coverage']
            merged[channel_str+'offsets'] += metrics[channel_str+'offsets']

    merged['total_average_offset'] = [mean(error) for error in zip(*merged['all_offsets'])]

    for channel_index in range(num_channels):
        channel_str = 'channel_{}_'.format(channel_index)
        merged[channel_str+'average_offset'] = [mean(error) for error in zip(*merged[channel_str+'offsets'])]

    return merged
