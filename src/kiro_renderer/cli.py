import argparse
import sys
from .core import render

def main():
    parser = argparse.ArgumentParser(description="Render a .kiro file to HTML.")
    parser.add_argument("input_file", help="Path to the input .kiro file.")
    parser.add_argument("-o", "--output", help="Path to the output HTML file. Defaults to stdout.")

    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            kiro_text = f.read()
        
        html_output = render(kiro_text)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(html_output)
            print(f"Successfully rendered {args.input_file} to {args.output}")
        else:
            sys.stdout.write(html_output)

    except FileNotFoundError:
        print(f"Error: Input file not found at {args.input_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
