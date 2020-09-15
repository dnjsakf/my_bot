data = [1, 2, 3, 4, 5]

def get_data():
    while data:
        yield data.pop()


gen = get_data()

print( next(gen) )
print( next(gen) )
print( next(gen) )
print( next(gen) )