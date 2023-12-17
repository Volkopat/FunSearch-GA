DEFINE scoring_function(buckets, bucket_limit) AS:
    SET total_empty_space TO 0
    FOR each bucket IN buckets DO:
        INCREMENT total_empty_space BY (bucket_limit - sum(bucket))
    ENDFOR
    
    SET score TO (1000 - total_empty_space) - (10 * number_of_buckets(buckets))
    RETURN score
