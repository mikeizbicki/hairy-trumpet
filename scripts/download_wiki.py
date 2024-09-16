'''
'''

import wikipedia

def get_wikipedia_contents(pagename, recursive_depth, debug_str=''):
    logging.info(debug_str + pagename)
    page = wikipedia.page(pagename, auto_suggest=False)
    content = page.content
    if recursive_depth > 0:
        logging.info(f"len(page.links)={len(page.links)}")
        for i, link in enumerate(page.links):
            debug_str2 = debug_str + f'({i}/{len(page.links)})'
            try:
                content += '\n\n' + get_wikipedia_contents(link, recursive_depth-1, debug_str2)
            except wikipedia.exceptions.PageError as e:
                logging.warning(e)

    return content


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page', default='2024_United_States_presidential_election')
    parser.add_argument('--output_dir', default='raw')
    parser.add_argument('--output_prefix', default='wiki_')
    parser.add_argument('--recursive_depth', type=int, default=0)
    args = parser.parse_args()

    import logging
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level='INFO',
        )

    content = get_wikipedia_contents(args.page, args.recursive_depth)
    output_path = args.output_dir + '/' + args.output_prefix + f'r{args.recursive_depth}_' + args.page
    with open(output_path, 'wt') as f:
        f.write(content)

