import re
import argparse
import tkinter as tk
from tkinter import filedialog
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

    if not args.input or not args.output:
        root = tk.Tk()
        root.withdraw()

        input_file = filedialog.askopenfilename(title='Select Input Text File', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
        output_file = filedialog.asksaveasfilename(title='Save As CSV File', defaultextension='.csv', filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')])

        root.destroy
        
    else:
        input_file = args.input
        output_file = args.output

    if input_file and output_file:
        convert_marker_file(input_file, output_file)
    else:
        print('Please select input and output files')

if __name__ == '__main__':
    main()
