# Cardinality Estimation using the Flajolet-Martin algorithm #
---
Imagine if you have data and you wish to know its cardinality (the number of unique elements present).Calcalating the cardinality can have multiple uses, e.g to count the number of unique visitors on a website. 

You could code a simple algorithm to loop through the dataset and check whether each element only occurs once or not, but this isn't feasible if you have a gigantic dataset with terabytes worth of data which can not even fit in your computer's memory. To solve this problem, one can use Cardinality Estimators which give a very close estimate of a dataset's cardinality at the cost of minimal memory usage.

## The Idea Behind it ##
---
Provided that you have a large dataset, the probability of seeing a hashed item (converted to its binary form) which ends with an *x* amount of zeroes is `2^x`. For example, if you need 3 zeroes at the end, the probability is `0.5 * 0.5 * 0.5 = 0.125` because each bit is either a 0 or a 1. Hence, on average, you would get one number with 3 zeroes at the end out of `1/0.5^x` numbers which is the equivalent of `2^x`. This is another simple method of estimating the cardinality, but it can give drastically inaccurate results if a hashed value has too many zeroes, and its estimates are in the power of 2 (256, 512, 1024...). One improvement on this method is to use various hash functions and average the estimates given to us, but a variety of hash functions is computationally expensive. To bypass this computational constraint, we can use a method called stochastic averaging where we divide the output of a single hash function into two parts. The number of buckets where we store the maximum number of 0's denoted by *m* and number of bits used to calculate which bucket we store our maximum number of 0's. The accuracy of this algorithm, according to the paper it is based on, boils down to 1.3/sqrt(m) where m is the number of buckets so depending on the accuracy you want, you can vary the value of m but not to extremely large values. The reason being that your value of *k* (which is the number of bits used in the hashed value to calculate the bucket index) is determined by log(m), and you don't want to use a large number of bits. For example, if you have a binary value of 10000100000 and you use a value of 1024 for m, then you only get 1 as the maximum number of 0's instead of 5.

An example of values for m/k for a binary input of 10010000 using *k* as 2 would result in using the left 2 most bits to calculate the bucket number (10 corresponds to bucket no.2) and using the remaining bits to count the number of ending 0's (which are 4 in this case), and then storing the number of ending 0's in that bucket.

**Note: This algorithm produces predictably larger estimates; hence, to correct for the bias, the final output is multiplied by a constant of 0.79402 which was derived through statistical analyses by Mariannae Durand and Phillipie Flajolet**

# Usage #
---
```python
import cardinality_cs110
data = ['sample data here']
print (cardinality_cs110.flajolet_martin(data,k))