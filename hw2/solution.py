#!/usr/bin/env python3

import os
import sys
import struct
import heapq
import tempfile
import multiprocessing

integer_size = 4

def read_integers_from_file(filename, offset, count):
    result = []
    with open(filename, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        raw_data = f.read(count * integer_size)
        result = list(struct.unpack("<" + "i" * count, raw_data))
    return result

def write_integers_to_file(filename, data):
    with open(filename, "wb") as f:
        f.write(struct.pack("<" + "i" * len(data), *data))

def sort_chunk(data):
    data.sort()
    return data

def parallel_sort_chunks(original_file, chunk_size, num_threads):
    temp_files = []
    file_size = os.path.getsize(original_file)
    total_numbers = file_size // integer_size
    
    num_chunks = (total_numbers + chunk_size - 1) // chunk_size
    
    pool = multiprocessing.Pool(processes=num_threads)
    async_results = []

    for i in range(num_chunks):
        offset = i * chunk_size * integer_size
        size_for_this_chunk = min(chunk_size, total_numbers - i * chunk_size)
        
        data_block = read_integers_from_file(original_file, offset, size_for_this_chunk)
        async_res = pool.apply_async(sort_chunk, (data_block,))
        async_results.append(async_res)
    
    for async_res in async_results:
        sorted_data = async_res.get()
        tmp_fd, tmp_path = tempfile.mkstemp(prefix="chunk_", suffix=".bin")
        os.close(tmp_fd)
        write_integers_to_file(tmp_path, sorted_data)
        temp_files.append(tmp_path)

    pool.close()
    pool.join()
    
    return temp_files

def merge_sorted_files(sorted_files, output_file):
    file_handlers = [open(f, "rb") for f in sorted_files]
    min_heap = []
    
    def read_next_int(fh, index):
        raw = fh.read(integer_size)
        if len(raw) < integer_size:
            return None
        val = struct.unpack("<i", raw)[0]
        return (val, index)
    
    for i, fh in enumerate(file_handlers):
        item = read_next_int(fh, i)
        if item is not None:
            heapq.heappush(min_heap, item)
    
    with open(output_file, "wb") as out:
        while min_heap:
            val, idx = heapq.heappop(min_heap)
            out.write(struct.pack("<i", val))
            next_item = read_next_int(file_handlers[idx], idx)
            if next_item is not None:
                heapq.heappush(min_heap, next_item)
        print(f"Результат сортировки сохранен в файл {output_file}")
    
    for fh in file_handlers:
        fh.close()
    for f in sorted_files:
        os.remove(f)

def external_sort(filename, chunk_size):
    num_threads = multiprocessing.cpu_count()
    print(f"Сортируем файл {filename}, чанки по {chunk_size} чисел, используем {num_threads} процессов.")

    temp_files = parallel_sort_chunks(filename, chunk_size, num_threads)
    
    directory = os.path.dirname(filename)
    base_name = os.path.basename(filename)
    out_name = os.path.join(directory, base_name + ".sorted.bin")
    
    merge_sorted_files(temp_files, out_name)
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python solution.py <input_file> <chunk_size>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    chunk_size = int(sys.argv[2])
    
    external_sort(input_file, chunk_size)
