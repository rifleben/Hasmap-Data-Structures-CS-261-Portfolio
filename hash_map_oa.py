
from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Input: Key (string) to be the "key" of our hashmap item, and value (object) to be the value
        Output: None
        Method updates the key/value pair in hashmap. If key already in hashmap, associate value will be replaced.
        If not in hashmap, key/value pair will be added.
        """

        # check to see if we need to resize table
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # create the HashEntry object with key/value given:
        hash_entry = HashEntry(key, value)

        attempt_idx = self._hash_function(key) % self._buckets.length()

        # if the first attempt index is available to be modified, then place the value there:
        if self._buckets[attempt_idx] is None or self._buckets[attempt_idx].is_tombstone is True:
            self._buckets[attempt_idx] = hash_entry
            self._size += 1
            return

        # if we just need to update key:
        if self._buckets[attempt_idx].key == key:
            self._buckets[attempt_idx] = hash_entry
            return

        j = 1
        # if the fist attempts are not removals or empty's we will probe further
        while self._buckets[attempt_idx]:
            attempt_idx = (self._hash_function(key) + j ** 2) % self._buckets.length()
            # If the value is empty or it's a Tombstone flagged we can place the valie there
            if self._buckets[attempt_idx] is None or self._buckets[attempt_idx].is_tombstone is True:
                self._buckets[attempt_idx] = hash_entry
                self._size += 1
                return
            # if they key exists, is not tombstone, we need to update it:
            if self._buckets[attempt_idx].key == key:
                self._buckets[attempt_idx] = hash_entry
                return
            # move onto next item in buckets if we didn't do anything
            j += 1

        # if nothing happens or is added we will return None:
        return None

    def table_load(self) -> float:
        """
        Input: None
        Return: Float
        Method returns the current hashtable load factor as a float.
        """

        # calculate the load factor using formula:
        load_factor = (self._size / self._capacity)

        # return float value:
        return load_factor

    def empty_buckets(self) -> int:
        """
        Input: None
        Output: Int of empty buckets
        Method checks for empty buckets in hashmap (including tombstone values)
        """

        return_val = 0
        # iterate through bucket to count empty or tombstone values:
        for entry in range(self._buckets.length()):
            # check if the idx is None or if there is a value in there, tombstone is True:
            if self._buckets[entry] is None or self._buckets[entry].is_tombstone is True:
                return_val += 1

        return return_val

    def resize_table(self, new_capacity: int) -> None:
        """
        Input: integer for new capacity
        Output: None
        Method resizes hashtable to new_capacity if new capacity isn't prime, new capacity modified to be prime
        """

        # first check if new_capacity < 1. If so exit via return.
        if new_capacity < self._size:
            return

        # if the new_cap is not already prime, we will make it prime with _next_prime():
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # set new capacity number
        self._capacity = new_capacity

        # make a reference to the current values in self_buckets
        copy_da = self._buckets

        # initialize a new empty DA to be the new buckets
        cleared_buckets = DynamicArray()

        # grow the empty the DA to the size of the existing using empty spaces:
        for idx in range(self._capacity):
            cleared_buckets.append(None)

        # replace the current buckets with the new DA and set size to reflect empty:
        self._buckets = cleared_buckets
        self._size = 0

        # populate the new buckets with the data from copy, less Tombstone flagged items
        for idx in range(copy_da.length()):
            if copy_da[idx] is not None:
                if copy_da[idx].is_tombstone is False:
                    self.put(copy_da[idx].key, copy_da[idx].value)

    def get(self, key: str) -> object:
        """
        Input: String (Key) to locate
        Output: Value of key
        Method returns value associated with given key. If key not in hash map, method returns None.
        """
        # if the size is zero we don't have anything to return:
        if self._size == 0:
            return None
        # if we check the first possible index it could be in, and it's empty, return None
        if not self._buckets[self._hash_function(key) % self._buckets.length()]:
            return None

        attempt_idx = self._hash_function(key) % self._buckets.length()

        if self._buckets[attempt_idx].key == key and self._buckets[attempt_idx].is_tombstone is True:
            return None

        j = 1
        # now we must probe to go further:
        while self._buckets[attempt_idx] is not None:
            # if we find a key that matches that is not a tombstone, return the value of that entry
            if self._buckets[attempt_idx].key == key and self._buckets[attempt_idx].is_tombstone is False:
                return self._buckets[attempt_idx].value
            # move onto next searchable index
            attempt_idx = (self._hash_function(key) + j ** 2) % self._buckets.length()
            j += 1

    def contains_key(self, key: str) -> bool:
        """
        Input Key to attempt to locate in Hash
        Output: Bool (True/False if value exists)
        Method returns True if given key is in the hashmap. Otherwise, returns false.
        """
        # if there is nothing in the map we can return False:
        if self._size == 0:
            return False

        j = 1
        attempt_idx = self._hash_function(key) % self._buckets.length()
        # check to see if the value exists at the expected hash:
        if self._buckets[attempt_idx] is not None:
            # While there is some value in the bucket
            while self._buckets[attempt_idx] is not None:
                # if the value exists and tombstone flag is false, we found the Key
                if self._buckets[attempt_idx].key == key and self._buckets[attempt_idx].is_tombstone is False:
                    return True
                # otherwise, we need to Quadratic probe further using the formula given in the explorations
                else:
                    attempt_idx = (self._hash_function(key) + j ** 2) % self._buckets.length()
                    j += 1

        # if nothing matching is found return False:
        return False

    def remove(self, key: str) -> None:
        """
        Input: Key value to attempt to remove (string)
        Output: None
        Method removes input key and associated value from the map. If key isn't in hashmap, method does nothing
        """
        # index to start with given key:
        attempt_idx = self._hash_function(key) % self._buckets.length()
        j = 1

        while self._buckets[attempt_idx] is not None:
            if self._buckets[attempt_idx].key == key and self._buckets[attempt_idx].is_tombstone is False:
                self._buckets[attempt_idx].is_tombstone = True
                self._size -= 1
                return

            attempt_idx = (self._hash_function(key) + j ** 2) % self._buckets.length()
            j += 1

    def clear(self) -> None:
        """
        Input: None
        Output: None
        Method clears the contents of the hashmap. Does not change underlying hash table capacity.
        """

        # initialize a new empty DA to be the new buckets
        cleared_buckets = DynamicArray()

        # grow the empty the DA to the size of the existing using empty spaces:
        for idx in range(self._capacity):
            cleared_buckets.append(None)

        # replace the current buckets with the new DA and set size to reflect empty:
        self._buckets = cleared_buckets
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Input: None
        Output: Dynamic Array
        Method returns a DA where each index contains a tuple of a key/value pair stored in the hash map
        """
        # initialize Dynamic Array
        return_da = DynamicArray()

        # for idx in the self_buckets DA:
        for idx in range(self._buckets.length()):
            if self._buckets[idx] is not None and self._buckets[idx].is_tombstone is False:
                return_da.append((self._buckets[idx].key, self._buckets[idx].value))
        return return_da

    def __iter__(self):
        """
        Create iterator for the next function to keep track of index we are on
        """
        # current index we are itterating through:
        self._index = 0

        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        # While we are not at the end of the DA
        while self._index < self._buckets.length():
            # grab our value and make increment index:
            value = self._buckets[self._index]
            self._index += 1

            # if the value is something other than None and isn't a tombstone we will return that
            if value and value.is_tombstone is False:
                return value

        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
