from __future__ import absolute_import, division, print_function

from analysis.shared.metadata import Metadata
import re

def load_metadata(filenames):
    metadatas = [Metadata.parse_metadatafile(input_json) for input_json in filenames]
    return sum(metadatas, Metadata())

def load_patterns(pattern, is_file):
    if is_file:
        with open(pattern, 'r') as text_file:
            return [line.strip() for line in text_file]
    else:
        return [pattern]

def grep(metadata, pattern, is_regex, is_file, is_inverted):
    patterns = load_patterns(pattern, is_file)

    if is_regex:
        return metadata.match(patterns, is_inverted)
    else:
        return metadata.find(patterns, is_inverted)

def run(inputs, pattern, is_regex, is_file, is_inverted):
    metadata = load_metadata(inputs)

    print(str(grep(metadata, pattern, is_regex, is_file, is_inverted)))
