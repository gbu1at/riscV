from setting import *



class CacheLine:
    def __init__(self, size) -> None:
        self.size = size
    def add(self, addres) -> bool:
        pass


class LruCacheLine(CacheLine):
    def __init__(self, size):
        super().__init__(size)
        self.lru_cache = {}
        self.access_order = []

    def add(self, address) -> bool:
        if address in self.lru_cache:
            self.access_order.remove(address)
            self.access_order.append(address)
            return True
        else:
            if len(self.lru_cache) >= self.size:
                lru = self.access_order.pop(0)
                del self.lru_cache[lru]
            self.lru_cache[address] = True
            self.access_order.append(address)
            return False

class BitpLruCacheLine(CacheLine):
    def __init__(self, size):
        super().__init__(size)
        self.mru = {}
        self.access_order = []
    
    def add(self, address) -> bool:
        if address in self.mru:
            return True
        elif address in self.access_order:
            if len(self.mru) == self.size - 1:
                self.mru = {}
            self.mru[address] = True
            return True
        else:
            if len(self.access_order) < self.size:
                self.access_order.append(address)
            else:
                for i, add in enumerate(self.access_order):
                    if add not in self.mru:
                        self.access_order[i] = address
                        break
            
            if len(self.mru) == self.size - 1:
                self.mru = {}
            self.mru[address] = True
            
            return False

class Cache:
    def __init__(self, cacheLine: CacheLine) -> None:
        self.caches = [cacheLine(CACHE_WAY) for i in range(CACHE_SETS)]
        self.cache_hit_instruction = 0
        self.cache_total_instruction = 0

        self.cache_hit_memory = 0
        self.cache_total_memory = 0
    
    def add(self, address: int, type="inst") -> bool:

        tag_address = address - address % CACHE_LINE_SIZE

        idx_adrress = (tag_address // CACHE_LINE_SIZE) % CACHE_SETS

        hit = self.caches[idx_adrress].add(tag_address)

        if type == "inst":
            self.cache_total_instruction += 1
            if hit:
                self.cache_hit_instruction += 1
        elif type == "mem":
            self.cache_total_memory += 1
            if hit:
                self.cache_hit_memory += 1
        else: assert(False)

        return hit
    
    def get_info(self):

        cache_total = self.cache_total_memory + self.cache_total_instruction
        cache_hit = self.cache_hit_instruction + self.cache_hit_memory
        all_percent = 100 * cache_hit / cache_total
        instruction_percent = 100 * self.cache_hit_instruction / self.cache_total_instruction
        memory_percent = float("nan") if self.cache_total_memory == 0 else 100 * self.cache_hit_memory / self.cache_total_memory

        return all_percent, instruction_percent, memory_percent


class LruCache(Cache):
    def __init__(self) -> None:
        super().__init__(LruCacheLine)


class BitpLruCache(Cache):
    def __init__(self) -> None:
        super().__init__(BitpLruCacheLine)

