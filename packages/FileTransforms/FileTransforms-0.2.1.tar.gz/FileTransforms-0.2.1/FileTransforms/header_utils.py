import os
import json


def load_headers(headers_filename):
    if not os.path.exists(headers_filename):
        return None

    with open(headers_filename) as headers_file:
        return json.load(headers_file)


def generate_header_lookup_dict(tokens_dict, normalize_func=None):
    header_map = {}

    if not normalize_func:
        def normalize_func(s): return s

    for k in tokens_dict:
        norm_k = normalize_func(k)
        if isinstance(tokens_dict[k], list):
            for val in tokens_dict[k]:
                header_map[normalize_func(val)] = norm_k
        else:
            header_map[normalize_func(tokens_dict[k])] = norm_k

    return header_map


def enumerate_headers(headers, tokens, start_idx=1):
    token_counts = {}
    for t in tokens:
        token_counts[t] = start_idx

    for i, header in enumerate(headers):
        if header in tokens:
            headers[i] = header + str(token_counts[header])
            token_counts[header] += 1

    return headers
