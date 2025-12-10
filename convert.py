#!/usr/bin/env python3
"""
Convert a Bridge Base hand viewer URL into a .lin file.

Usage:
    python convert.py <bridge_base_url> [output_file]

Example:
    python convert.py "https://www.bridgebase.com/tools/handviewer.html?lin=pn%7C..." output.lin
"""

import sys
import urllib.parse
from pathlib import Path


def extract_lin_from_url(url):
    """
    Extract the LIN data from a Bridge Base hand viewer URL.

    Args:
        url: Bridge Base hand viewer URL containing lin parameter

    Returns:
        The decoded LIN string

    Raises:
        ValueError: If URL is invalid or doesn't contain lin parameter
    """
    parsed = urllib.parse.urlparse(url)

    if 'bridgebase.com' not in parsed.netloc:
        raise ValueError("URL must be from bridgebase.com")

    query_params = urllib.parse.parse_qs(parsed.query)

    if 'lin' not in query_params:
        raise ValueError("URL must contain 'lin' parameter")

    lin_data = query_params['lin'][0]
    decoded_lin = urllib.parse.unquote(lin_data)

    return decoded_lin


def convert_url_to_lin_file(url, output_file=None, append=True):
    """
    Convert a Bridge Base URL to a .lin file.

    Args:
        url: Bridge Base hand viewer URL
        output_file: Optional output file path. If not provided, will use 'hands.lin'
        append: If True, append to existing file. If False, overwrite. Default is True.

    Returns:
        Path to the created .lin file
    """
    lin_data = extract_lin_from_url(url)

    if output_file is None:
        output_file = 'hands.lin'

    output_path = Path(output_file)

    if not output_path.suffix:
        output_path = output_path.with_suffix('.lin')

    if append:
        with open(output_path, 'a', encoding='utf-8') as f:
            if output_path.exists() and output_path.stat().st_size > 0:
                f.write('\n')
            f.write(lin_data)
    else:
        output_path.write_text(lin_data, encoding='utf-8')

    return output_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nError: No URL provided")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        file_existed = Path(output_file if output_file else 'hands.lin').exists()
        output_path = convert_url_to_lin_file(url, output_file)

        if file_existed:
            print(f"Successfully appended hand to {output_path}")
        else:
            print(f"Successfully created {output_path}")

        print(f"Total file size: {output_path.stat().st_size} bytes")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()