import re
import argparse
from decimal import Decimal

def convert_marker_file(input_file, output_file):
    with open(input_file, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    converted_lines = ['#,Name,Start,End,Length\n']
    counter = 1
    for line in lines:
        if line.startswith('Marker file version') or line.startswith('Time format'):
            continue

        match = re.match(r'(\d\d)?_?([\w\s]+)\t(\d\d:\d\d:\d\d\.\d+)(\t(\d\d:\d\d:\d\d\.\d+))?', line)
        if match:
            name = match.group(2) if match.group(1) is None else f"{match.group(1)}_{match.group(2)}"
            start = match.group(3)
            end = match.group(5) if match.group(5) else ''
            length = ''

            if end:
                h1, m1, *s1 = map(Decimal, start.split(':') + start.split(':')[-1].split('.'))
                h2, m2, *s2 = map(Decimal, end.split(':') + end.split(':')[-1].split('.'))
                s1 = s1[0] if s1 else Decimal(0)
                s2 = s2[0] if s2 else Decimal(0)
                length_seconds = (h2 - h1) * 3600 + (m2 - m1) * 60 + (s2 - s1)
                length = f'{int(length_seconds // 60):02d}:{int(length_seconds % 60):02d}.{int(length_seconds % 1 * 1000):03d}'
                start = f'{int(h1):02d}:{int(m1):02d}:{s1:06.3f}'
                end = f'{int(h2):02d}:{int(m2):02d}:{s2:06.3f}'

            converted_lines.append(f'R{counter},"{name}",{start},{end},{length}\n')
            counter += 1
        else:
            length = ''
            converted_lines.append(f'M{counter},"",{length}\n')
            counter += 1

    with open(output_file, 'w', encoding="utf-8") as f:
        f.writelines(converted_lines)

def main():
    parser = argparse.ArgumentParser(description='Convert marker text file to CSV format')
    parser.add_argument('-i', '--input', help='Input text file', required=False)
    parser.add_argument('-o', '--output', help='Output CSV file', required=False)

    args = parser.parse_args()

    if args.input and args.output:
        convert_marker_file(args.input, args.output)
    else:
        print('This script makes to convert RX marker and region list file to reaper csv.:')
        print('Convert then Go to action list and search Markers/Regions: Import markers/regions from file.:')
        print('Please type:')
        print('python rxtocsv.py -i your_input_file.txt -o your_output.csv')

if __name__ == '__main__':
    main()
