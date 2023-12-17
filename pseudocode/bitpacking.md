Initialize a list of buckets, each with a fixed capacity
FOR each bit sequence to be packed:
    FOR each bucket:
        IF the bit sequence fits in the bucket (without exceeding the bucket's capacity):
            Pack the bit sequence into the bucket
            BREAK out of the loop (go to the next bit sequence)
    IF no suitable bucket is found:
        Create a new bucket
        Pack the bit sequence into the new bucket
Return the list of buckets
