import argparse
import sys
from kiro_renderer import render

def main():
    parser = argparse.ArgumentParser(description="Render a .kiro file to HTML.")
    parser.add_argument("input_file", help="Path to the input .kiro file.")
    parser.add_argument("-o", "--output", help="Path to the output HTML file. Defaults to stdout.")

    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            kiro_text = f.read()
        
        html_output, css_output = render(kiro_text)

        if args.output:
            html_file_path = args.output
            css_file_path = html_file_path.replace(".html", ".css") # Assuming .html extension

            with open(html_file_path, 'w', encoding='utf-8') as f:
                f.write(html_output)
            print(f"Successfully rendered HTML to {html_file_path}")

            with open(css_file_path, 'w', encoding='utf-8') as f:
                f.write(css_output)
            print(f"Successfully generated CSS to {css_file_path}")
        else:
            sys.stdout.buffer.write(html_output.encode('utf-8'))

    except FileNotFoundError:
        print(f"Error: Input file not found at {args.input_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
