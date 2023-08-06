import random

def zero_counter(number):
    """Counts the number of consecutive 0's at the end of the number"""
    x = 0
    while (number >> x) & 1 == 0:
        x = x + 1
    return x

def flajolet_martin(data, k):
    """Estimates the number of unique elements in the input set values.

    Inputs:
    data: The data for which the cardinality has to be estimated.
    k: The number of bits of hash to use as a bucket number. The number of buckets is 2^k
    
    Output:
    Returns the estimated number of unique items in the dataset
    """
    total_buckets = 2 ** k
    total_zeroes = []
    for i in range(total_buckets):
        total_zeroes.append(0)
    for i in data:
        h = hash(str(i)) #convert the value into a string because python hashes integers to themselves
        bucket = h & (total_buckets - 1) #Finds the bucket where the number of ending zero's are appended 
        bucket_hash = h >> k #move the bits of the hash to the right to use the binary digits without the bucket digits 
        total_zeroes[bucket] = max(total_zeroes[bucket], zero_counter(bucket_hash))
    return 2 ** (float(sum(total_zeroes)) / total_buckets) * total_buckets * 0.79402