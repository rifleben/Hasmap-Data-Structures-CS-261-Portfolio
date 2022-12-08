from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        If not in hashmap, key/value pair will be added
        """
        # check to see if it needs to be resized
        if int(self.table_load()) >= 1:
            self.resize_table(self._capacity * 2)

        list = self._buckets[self._hash_function(key) % self._capacity]

        # if the key already exists:
        if list.contains(key):
            # using contains key to return that node and modify its value
            list.contains(key).value = value
            return

        # otherwise add it to map:

        list.insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Input: None
        Output: Int of empty buckets
        Method checks for empty buckets in hashmap
        """
        # initializing return value variable:
        return_val = 0

        # for index in array, check if that linkedlist in array slot is empty (len == 0):
        for idx in range(self._buckets.length()):
            if self._buckets[idx].length() == 0:
                # if the LL is empty (len == 0), return value is incremented
                return_val += 1

        return return_val

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
            cleared_buckets.append(LinkedList())

        # replace the current buckets with the new DA and set size to reflect empty:
        self._buckets = cleared_buckets
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Input:
        Output: None
        Method resizes table
        Method changes capacity of hash table. All existing key/value pairs will remain in the new map.
        """

        # first check if new_capacity < 1. If so exit via return.
        if new_capacity < 1:
            return

        # if the new_cap is not already prime, we will make it prime with _next_prime():
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # copy current data and change capacity
        copy_buckets = self._buckets
        self._capacity = new_capacity

        # (essentially same as clear function here)
        # initialize a new empty DA to be the new buckets
        cleared_buckets = DynamicArray()

        # grow the empty the DA to the size of the existing using empty spaces:
        for idx in range(self._capacity):
            cleared_buckets.append(LinkedList())

        # replace the current buckets with the new DA and set size to reflect empty:
        self._buckets = cleared_buckets
        self._size = 0

        # go through current buckets and rehash those items into our new DA (future self._buckets):
        for idx in range(copy_buckets.length()):
            if copy_buckets[idx].length() != 0:
                ll = copy_buckets[idx]
                for node in ll:
                    self.put(node.key, node.value)

    def get(self, key: str):
        """
        Input: String (Key) to locate
        Output: Value of key
        Method returns value associated with given key. If key not in hash map, method returns None.
        """
        # if value not in map return None (edge case):
        if not self._buckets[self._hash_function(key) % self._buckets.length()].contains(key):
            return None
        else:
            return self._buckets[self._hash_function(key) % self._buckets.length()].contains(key).value

    def contains_key(self, key: str) -> bool:
        """
        Input Key to attempt to locate in Hash
        Output: Bool (True/False if value exists)
        Method returns True if given key is in the hashmap. Otherwise, returns false.
        """

        # empty hashmap doesn't contain keys, thus False:
        if self._size == 0:
            return False

        # check if the LinkedList at the hash function index contains key:
        if self._buckets[self._hash_function(key) % self._buckets.length()].contains(key):
            return True
        # otherwise if not there, item is key is not in map
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Input: Key value to attempt to remove (string)
        Output: None
        Method removes input key and associated value from the map. If key isn't in hashmap, method does nothing
        """
        # if the value exists in the buckets: remove it and decrement the size:
        if self._buckets[self._hash_function(key) % self._buckets.length()].contains(key):
            self._buckets[self._hash_function(key) % self._buckets.length()].remove(key)
            self._size -= 1

        return

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
            # check if the linked list at the current index is empty or not:
            if self._buckets[idx].length() != 0:
                # iterate through each node in the LinkedList
                for ll_node in self._buckets[idx]:
                    # append the values as a tuple:
                    return_da.append((ll_node.key, ll_node.value))
        return return_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Input: Dynamic Array:
    Output: Tuple(DA, int) Dynamic array will contain the value(s) of the DA that occur the most
    Function returns mode value(s) and the occurrence within the DA. uses a Map for calculation.
    """
    # init map to hold the frequency of each value in da (val, freq)
    map = HashMap()

    return_da = DynamicArray()
    highest_freq = 0

    # iterate through the DA:
    for idx in range(da.length()):
        # if map contains an object found in array increment value by 1:
        if map.contains_key(da[idx]):
            map.put(da[idx], map.get(da[idx]) + 1)
        # if not, then add that value to the map:
        else:
            map.put(da[idx], 1)
        # update highest_freq if value in map is higher
        if map.get(da[idx]) > highest_freq:
            highest_freq = map.get(da[idx])

    # get the contents of map, and store as variable:
    content = map.get_keys_and_values()

    # iterate through content
    for idx in range(content.length()):
        # if the value of the key value pair is == to highest_freq:
        if content[idx][1] == highest_freq:
            # We add that key to the return_da:
            return_da.append(content[idx][0])

    return return_da, highest_freq


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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
