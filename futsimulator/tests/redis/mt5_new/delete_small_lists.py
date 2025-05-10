import redis

# Connect to Redis
r = redis.Redis(host='192.168.1.48', port=6379, db=0)

# Scan through all keys
cursor = 0
keys_deleted = 0
threshold_size = 1_048_576  # 1 MB in bytes

while True:
    cursor, keys = r.scan(cursor)
    for key in keys:
        size = r.memory_usage(key)  # Get key size in bytes
        if size and size < threshold_size:
            r.delete(key)
            keys_deleted += 1

    if cursor == 0:  # If scan is complete, break
        break

print(f"Deleted {keys_deleted} keys smaller than 1MB.")
