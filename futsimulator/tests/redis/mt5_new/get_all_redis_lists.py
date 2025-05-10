import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Get all keys
cursor = 0
lists = []

while True:
    cursor, keys = r.scan(cursor)  # Efficient scanning of keys
    for key in keys:
        if r.type(key) == b'list':  # Check if the key is a list
            lists.append(key.decode())

    if cursor == 0:  # If scan is complete, break
        break

# Print retrieved lists
f_list = []
for key in lists:

    #print(f"List Key: {key}")
    if 'EP_202307' in key:
        f_list.append(key)
#        print(f"List Key: {key}")
    elif 'EP_202308' in key:
        f_list.append(key)
#        print(f"List Key: {key}")

f_list = sorted(f_list)
for key in f_list:
    print(f"List Key: {key}")