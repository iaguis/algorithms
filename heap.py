class Heap:
    def __init__ (self):
        self.a = [-1]
        self.dictionary = {}

    def swim (self, k):
        while k > 1 and self.greater(k/2, k):
            self.swap(k, k/2)
            k = k/2

    def sink (self, k):
        N = len(self.a) - 1
        while 2*k <= N:
            j = 2*k
            if j < N and self.greater(j, j+1):
                j += 1
            if not self.greater(k, j):
                break
            self.swap (k, j)
            k = j

    def has_key (self, x):
        return x in self.dictionary

    def isEmpty (self):
        return len(self.a) == 1

    def insert (self, x):
        self.a.append(x)
        self.dictionary[x.vertex] = len(self.a) - 1
        self.swim (len(self.a) - 1)

    def delMin (self):
        N = len(self.a) - 1
        minimum = self.a[1]
        self.swap (1, N)
        self.a.pop()
        del self.dictionary[minimum.vertex]
        self.sink(1)
        return minimum

    def delete (self, x):
        N = len(self.a) - 1
        pos = self.dictionary[x]
        element = self.a[pos]
        self.swap (pos, N)
        self.a.pop()
        del self.dictionary[element.vertex]
        self.sink(pos)
        return element

    def greater (self, i, j):
        return self.a[i].priority > self.a[j].priority

    def swap (self, i, j):
        tmp = self.dictionary[self.a[i].vertex]
        self.dictionary[self.a[i].vertex] = self.dictionary[self.a[j].vertex]
        self.dictionary[self.a[j].vertex] = tmp

        self.a[i], self.a[j] = self.a[j], self.a[i]

