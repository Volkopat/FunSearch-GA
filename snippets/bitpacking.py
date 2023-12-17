def number_packing(numbers, bucket_limit):
    """
    Packs numbers into the fewest number of buckets without exceeding the bucket limit.
    
    Parameters:
    numbers (list of int): A list of numbers to be packed.
    bucket_limit (int): The maximum sum allowed for each bucket.
    
    Returns:
    list of list: A list of buckets with packed numbers.
    """
    buckets = []  # Initialize the list of buckets

    # Iterate over each number
    for number in numbers:
        # Flag to check if number is packed
        packed = False
        
        # Try to fit the number into existing buckets
        for bucket in buckets:
            # Check if the number fits in the current bucket
            if sum(bucket) + number <= bucket_limit:
                bucket.append(number)  # Pack the number into the bucket
                packed = True
                print(f"Packed number {number} into existing bucket: {bucket}")
                break  # Break out of the loop as we've packed the number
        
        # If the number did not fit in any existing bucket, create a new bucket
        if not packed:
            buckets.append([number])
            print(f"Created new bucket for number {number}")
    
    # Display the packed buckets visually
    print("\nPacked Buckets:")
    for i, bucket in enumerate(buckets):
        print(f"Bucket {i+1}: {bucket} (Total: {sum(bucket)})")
    
    return buckets

# Example usage:
numbers_to_pack = [10, 20, 50, 5, 30, 60, 90, 15, 5, 1]
bucket_limit = 100  # Each bucket can hold a sum of 100
buckets = number_packing(numbers_to_pack, bucket_limit)

# Output the result
print("\nFinal packed buckets:", buckets)
