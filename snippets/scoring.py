def scoring_function(buckets, bucket_limit):
    """
    Scores the packing efficiency based on the empty space and the number of buckets used.
    
    Parameters:
    buckets (list of list): A list of buckets with packed numbers.
    bucket_limit (int): The maximum sum allowed for each bucket.
    
    Returns:
    int: The score representing the packing efficiency.
    """
    # Calculate the total empty space across all buckets
    total_empty_space = sum(bucket_limit - sum(bucket) for bucket in buckets)
    
    # Calculate the score with a penalty for each bucket used
    score = (1000 - total_empty_space) - (10 * len(buckets))
    
    return score

# Example usage:
buckets = [[10, 20, 50, 5, 15], [30, 60, 5, 1], [90]]  # From the previous packing example
bucket_limit = 100
score = scoring_function(buckets, bucket_limit)

# Output the result
print(f"Packing efficiency score: {score}/1000")