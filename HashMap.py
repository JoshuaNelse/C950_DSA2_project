class HashMap:

    #######
    # O(1) - constant
    # create map with a size of 64 indexes by default
    def __init__(self, size=64):
        self.size = size
        self.map = [None] * self.size

    #######
    # O(N) - linear
    # creates/retrieves the hash value for a specified key value
    def _get_hash(self, key):
        _hash = 0
        if type(key) == int:
            return key % self.size
        for char in key:
            _hash += ord(char)
        return _hash % self.size

    #######
    # ~ O(1) - constant
    # uses the key hash to insert the item in constant time. Also handles collision
    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value_pair = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value_pair])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(key_value_pair)
            return True

    #######
    # ~ O(1) - constant
    # uses hash value of key to get value in constant time
    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is None:
            error = 'Key: \"{}\" not found in hash map.'.format(key)
            raise Exception(error)

        if len(self.map[key_hash]) == 1:
            return self.map[key_hash][0][1]
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]

    #######
    # ~ O(1) - constant
    # uses hash key value to delete value in constant time
    def delete(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is None:
            return False
        for index in range(len(self.map[key_hash])):
            if self.map[key_hash][index][0] == key:
                self.map[key_hash].pop(index)
                return True

    #######
    # O(1) - constant
    # finds distance between 2 locations in constant time. (requires 2d map)
    def get_distance(self, from_location, to_location):
        return self.get(from_location).get(to_location)

    #######
    # O(N^2) - quadratic
    # prints contents of the hashmap
    def print(self):
        for i in self.map:
            if i is None:
                continue

            for j in i:
                print("[Start: {}, Destinations: {}".format(j[0], j[1]))

    #######
    # O(1) - constant
    # returns the iterator for this object
    def __iter__(self):
        return self.map.__iter__()

    #######
    # O(N^2) - quadratic
    # defining single entry "to string" function
    def __str__(self):
        string_of = ''
        for i in range(0, len(self.map)):

            if self.map[i] is None:
                continue

            for j in self.map[i]:
                string_of_values = '[{}, {}]'.format(j[0], j[1])

                string_of += string_of_values
        return string_of


