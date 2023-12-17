def optimized_bucket_filler(numbers, bucket_limit):
    # Sort the list of numbers in descending order
    numbers = sorted(numbers, reverse=True)
    buckets = []

    # Loop through each number in the sorted list
    for number in numbers:
        # Try to place the number in an existing bucket
        placed = False
        for bucket in buckets:
            if sum(bucket) + number <= bucket_limit:
                bucket.append(number)
                placed = True
                break

        # If the number was not placed, create a new bucket
        if not placed:
            buckets.append([number])

    return buckets

print(optimized_bucket_filler([12, 58, 23, 97, 34, 86, 50, 29] , 100))