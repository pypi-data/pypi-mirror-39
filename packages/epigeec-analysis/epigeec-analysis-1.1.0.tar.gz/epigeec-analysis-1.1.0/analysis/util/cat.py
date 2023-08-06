from __future__ import absolute_import, division, print_function

import sys, argparse
from analysis.shared.metadata import Metadata

def run(inputs):
    metadatas = [Metadata.parse_metadatafile(input_json) for input_json in inputs]
    print(str(sum(metadatas, Metadata())))
