class Item():
    def __init__(self, key, data):
        self.key = key
        self.data = data

    def __str__(self):
        return self.data

class Hashmap():
    """A hashmap with lists as its buckets"""
    def __init__(self):
        self.array_length = 16
        self.hash_table = [[] for _ in range(self.array_length)]
        self.item_count = 0

    def __str__(self):
        """A str function to reveal the answer
        Time complexity O(n^2)"""
        string = ""
        for letter_list in self.hash_table:
            for letter in letter_list:
                string += str(letter.data)

        return string

    def find(self, key):
        i = hash(key) % self.array_length
        for item in self.hash_table[i]:
            if item.key == key:
                return item.data
        return None

    def __setitem__(self, key, data):
        i = hash(key) % self.array_length
        if self.find(i) == None:
            self.hash_table[i].append(Item(key, data))
            self.item_count += 1
        else:
            self.hash_table[i].append(Item(key, data))

    def __getitem__(self, key):
        return self.find(key)

    def __len__(self):
        return self.item_count

if __name__ == "__main__":
    string = "kristofer"
    hm = Hashmap()
    for num, letter in enumerate(string):
        hm[num] = letter

    hm[1] = "m" #collision! hash(1) % self.item_count = 3
    print(hm[1]) #krimstofer 

    print(hm)


