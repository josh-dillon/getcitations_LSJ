#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import re
import glob
import os

# Prompt user for author and work numbers.
# For example, enter "0011" for Sophocles and "005" for Electra.
while True:
    author_code = input("Enter the four-digit author number (e.g. 0011): ").strip()
    if re.fullmatch(r"\d{4}", author_code):
        break
    else:
        print("Invalid number. Please enter exactly four digits.")

while True:
    work_code = input("Enter the three-digit work number (e.g. 005): ").strip()
    if re.fullmatch(r"\d{3}", work_code):
        break
    else:
        print("Invalid number. Please enter exactly three digits.")

# Build the regular expression pattern dynamically using an f-string.
bibl_pattern = re.compile(
    rf"^Perseus:abo:tlg,{author_code},{work_code}:(?:(\d+[a-zA-Z]?)|(\d+):(\d+))$"
)

# Define the directory containing the XML files.
input_dir = "/path/to/LSJ"
if not input_dir.endswith(os.sep):
    input_dir += os.sep

# List to hold tuples of (sort_key, number_string, head_text).
results = []

def natural_sort_key(s):
    """
    Returns a tuple to sort citation strings naturally.
    
    For composite citations (with a full stop) like "8.87":
      - We expect s to have the format "major.minor" (both parts digits),
      - and return a tuple (major, 0, minor) where both are integers.
    
    For single-group citations like "27" (straight line numbers) or "27a" (Stephanus):
      - We match digits with an optional letter.
      - Pure numbers (with no letter) return (number, 0, 0)
      - If a letter is present, we return (number, 1, letter)
        so that, for instance, "27" sorts before "27a".
    """
    if '.' in s:
        parts = s.split('.', 1)
        if parts[0].isdigit() and parts[1].isdigit():
            return (int(parts[0]), 0, int(parts[1]))
    m = re.match(r"^(\d+)([a-zA-Z]?)$", s)
    if m:
        num = int(m.group(1))
        letter = m.group(2)
        if letter == "":
            return (num, 0, 0)
        else:
            return (num, 1, letter)
    # Fallback: send things that don't match to the end.
    return (float('inf'), 0, 0)

# Process all XML files in the input directory.
for filepath in glob.glob(f"{input_dir}*.xml"):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as err:
        print(f"Error parsing {filepath}: {err}")
        continue

    # Find all <div2> elements.
    for div2 in root.findall(".//div2"):
        head_elem = div2.find("head")
        if head_elem is None or head_elem.text is None:
            continue
        head_text = head_elem.text.strip()

        # Look for all <bibl> elements within the div.
        for bibl in div2.findall(".//bibl"):
            n_attr = bibl.get("n", "")
            m = bibl_pattern.match(n_attr)
            if m:
                # If group(1) is present, we have the single-number case.
                if m.group(1):
                    number_str = m.group(1)
                # Otherwise, if groups 2 and 3 are present, it's the composite case.
                elif m.group(2) and m.group(3):
                    # Join the two numbers with a full stop.
                    number_str = f"{m.group(2)}.{m.group(3)}"
                else:
                    continue

                # Save the tuple (sort key, the number string, and head text).
                results.append((natural_sort_key(number_str), number_str, head_text))

# Remove dupes and sort the results by the computed sort key.
unique_results = sorted(set(results), key=lambda x: x[0])

# Write the output to a text file.
output_filename = "output.txt"
with open(output_filename, "w", encoding="utf-8") as out_file:
    for _, number_str, head_text in unique_results:
        out_file.write(f"{number_str}\t{head_text}\n")

print(f"Extraction complete. Results written to {os.path.abspath(output_filename)}")
