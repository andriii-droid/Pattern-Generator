class ID():
    '''Implements a class to keep track of ids'''
    def __init__(self):
        self._active_ids = []
        self._next_id = 1

    @property
    def new_id(self):
        '''returns a new id'''
        new_id = self._next_id
        self._active_ids.append(new_id)
        self._next_id = self._calc_next_id()
        return new_id

    @property
    def active_ids(self):
        '''returns all active ids in a sorted list'''
        self._active_ids.sort()
        return self._active_ids

    def return_id(self, id):
        '''is called to return a id'''
        self._active_ids.remove(id)
        self._next_id = self._calc_next_id()

    def _calc_next_id(self):
        '''searches the next unused id'''
        iterator = 1
        while (iterator in self._active_ids):
            iterator += 1
        return iterator
if __name__ == '__main__':

    id = ID()
    id1 = id.new_id
    id2 = id.new_id
    id3 = id.new_id    
    id4 = id.new_id
    print(id.active_ids)
    id.return_id(id3)
    print(id.active_ids)
    id5 = id.new_id    
    print(id.active_ids)
