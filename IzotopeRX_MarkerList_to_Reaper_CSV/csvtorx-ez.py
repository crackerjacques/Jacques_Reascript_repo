import argparse
import easygui
from decimal import Decimal

def convert_csv_to_text(input_file, output_file):
    with open(input_file, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    converted_lines = ['Marker file version: 1\n', 'Time format: Time\n']
    for line in lines[1:]:
        parts = line.strip().split(',')
        if len(parts) == 5:
            _, name, start, end, _ = parts
            name = name.strip('"')
            if end:
                converted_lines.append(f'{name}\t{start}\t{end}\n')
            else:
                converted_lines.append(f'{name}\t{start}\n')

    with open(output_file, 'w', encoding="utf-8") as f:
        f.writelines(converted_lines)

def main():
    parser = argparse.ArgumentParser(description='Convert CSV file back to marker text format')
    parser.add_argument('-i', '--input', help='Input CSV file', required=False)
    parser.add_argument('-o', '--output', help='Output text file', required=False)

    args = parser.parse_args()

    if not args.input or not args.output:
        input_file = easygui.fileopenbox(title='Select Input CSV File')
        output_file = easygui.filesavebox(title='Save As Text File', default='*.txt')
    else:
        input_file = args.input
        output_file = args.output

    if input_file and output_file:
        convert_csv_to_text(input_file, output_file)
    else:
        print('Please select input and output files')

if __name__ == '__main__':
    main()
