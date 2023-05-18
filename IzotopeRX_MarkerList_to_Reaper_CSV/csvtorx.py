import argparse
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
    parser.add_argument('-i', '--input', help='Input CSV file', required=True)
    parser.add_argument('-o', '--output', help='Output text file', required=True)

    args = parser.parse_args()

    if args.input and args.output:
        convert_csv_to_text(args.input, args.output)
    else:
        print('This script makes to convert reaper csv to RX marker and region list file.:')
        print('Convert then Go to Window -> Markers and Regions and Import Marker file. :')
        print('Please type:')
        print('python csvtorx.py -i your_input_file.csv -o your_output.txt')

if __name__ == '__main__':
    main()
