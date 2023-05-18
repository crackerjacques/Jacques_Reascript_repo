import struct
from reapy_boost import reascript_api as RPR
import re

# This script reads the marker embedded in the wav file and splits them.
# Select the file you wish to process and run it from a terminal or command prompt.
# Running it from outside Reaper is slower than running it from inside Reaper.


def read_chunks(file):
    cue_points = {}
    sample_rate = None

    while True:
        chunk_id = file.read(4)
        if not chunk_id:  # EOF
            break

        try:
            chunk_size, = struct.unpack('<I', file.read(4))
        except struct.error:  
            break

        chunk_data = file.read(chunk_size)

        print(f'Chunk: id={chunk_id}, size={chunk_size}')

        if chunk_id == b'fmt ':
            sample_rate = parse_fmt_chunk(chunk_data)
            print(f'Sample rate: {sample_rate}')

        elif chunk_id == b'cue ':
            cue_points = parse_cue_chunk(chunk_data)

        elif chunk_id == b'LIST':
            parse_list_chunk(chunk_data, cue_points)

    return cue_points, sample_rate

def parse_fmt_chunk(data):
    sample_rate, = struct.unpack('<I', data[4:8])
    return sample_rate

def parse_cue_chunk(data):
    cue_points_count, = struct.unpack('<I', data[:4])
    print(f'  Cue points: {cue_points_count}')

    cue_points = {}
    for i in range(cue_points_count):
        start = 4 + i * 24
        cue_data = data[start : start + 24]
        cue_id, position, data_chunk_id, chunk_start, block_start, sample_offset = struct.unpack('<II4sIII', cue_data)
        print(f'    Cue point {i + 1}:')
        print(f'      ID: {cue_id}')
        print(f'      Position: {position}')
        print(f'      Data chunk ID: {data_chunk_id}')
        print(f'      Chunk start: {chunk_start}')
        print(f'      Block start: {block_start}')
        print(f'      Sample offset: {sample_offset}')
        cue_points[cue_id] = {'Position': position, 'Type': data_chunk_id.decode()}  # Added type

    return cue_points

def parse_list_chunk(data, cue_points):
    if data[:4] != b'adtl':
        return
    data = data[4:]
    while data:
        subchunk_id = data[:4]
        subchunk_size, = struct.unpack('<I', data[4:8])
        subchunk_data = data[8:8+subchunk_size]

        if subchunk_id == b'ltxt':
            parse_ltxt_chunk(subchunk_data, cue_points)
        elif subchunk_id == b'labl':
            parse_labl_chunk(subchunk_data, cue_points)

        data = data[8+subchunk_size:]

def parse_labl_chunk(data, cue_points):
    cue_id, = struct.unpack('<I', data[:4])
    name = data[4:].decode().rstrip('\x00')
    if cue_id in cue_points:
        cue_points[cue_id]['Name'] = name
        print(f'    Cue point {cue_id}:')
        print(f'      Name: {name}')


def parse_ltxt_chunk(data, cue_points):
    cue_id, length = struct.unpack('<II', data[:8])
    if cue_id in cue_points:
        cue_points[cue_id]['Length'] = length
        print(f'    Cue point {cue_id}:')
        print(f'      Length: {length}')
        print(f'      End Position: {cue_points[cue_id]["Position"] + length}')

def get_mediapath():
    num_selected_items = RPR.CountSelectedMediaItems(0)
    
    if num_selected_items > 0:

        selected_item = RPR.GetSelectedMediaItem(0, 0)       
        take = RPR.GetActiveTake(selected_item)
        
        if take is not None:
            source = RPR.GetMediaItemTake_Source(take)
            file_path_buffer = '\0' * 512
            _, file_path, _ = RPR.GetMediaSourceFileName(source, file_path_buffer, len(file_path_buffer))

            return file_path 

file_path = get_mediapath()
print(file_path)

selected_item = RPR.GetSelectedMediaItem(0, 0)

item_start_position = RPR.GetMediaItemInfo_Value(selected_item, "D_POSITION")

def get_sample_rate_from_path(file_path):
    match = re.search(r'(\d+\.?\d*) kHz', file_path)
    if match:
        sample_rate_str = match.group(1).replace('.', '') + '000'
        return int(sample_rate_str)

def samples_to_time(samples, sample_rate):
    if sample_rate is None:
        print("Sample rate not found. Defaulting to 48000 Hz.")
        sample_rate = 48000
    return samples / sample_rate

selected_item = RPR.GetSelectedMediaItem(0, 0)

item_start_position = RPR.GetMediaItemInfo_Value(selected_item, "D_POSITION")

# Open the file in binary mode
with open(file_path, 'rb') as file:
    # Skip the RIFF header
    file.read(12)

    cue_points, sample_rate = read_chunks(file)

# Skip cue points with "Length"

for cue_id, cue_point in cue_points.items():
    if 'Length' in cue_point:
        continue  

    print(f'Cue point {cue_id}:')
    start_sample = cue_point["Position"]
    print(f'  Start Position (sample): {start_sample}')

    start_time = samples_to_time(start_sample, sample_rate) + item_start_position

    RPR.SetEditCurPos(start_time, True, True)
    RPR.Main_OnCommand(40012, 0) 

