'''
Download raw wikipedia articles (possibly recusively) in a format suitable for generating cloze datasets.
'''

import wikipedia


def get_wikipedia_contents(pagenames, recursive_depth=0):
    '''
    Recursively download all the contents of a wikipedia page and any linked pages.
    All of the contents are appended into the single output string.
    '''
    import wikipedia
    for i, pagename in enumerate(pagenames):
        logging.info(f'downloading ({i}/{len(pagenames)}) pagename="{pagename}"')
        try:
            page = wikipedia.page(pagename, auto_suggest=False)
            content = page.content
            yield f'= {pagename} ='
            yield ''
            for line in content.split('\n'):
                yield line

            if recursive_depth > 0:
                logging.debug(f"len(page.links)={len(page.links)}")
                yield from get_wikipedia_contents(page.links, recursive_depth-1)

        # the following errors are raised when wikipedia doesn't have content for the specified name;
        # in that event, we just record the error and continue with the next pagename
        except wikipedia.exceptions.DisambiguationError:
            logging.debug(f'DisambiguationError')
        except wikipedia.exceptions.PageError:
            logging.debug(f'PageError')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page')
    parser.add_argument('--pages_file')
    parser.add_argument('--output_dir', default='raw')
    parser.add_argument('--recursive_depth', type=int, default=0)
    args = parser.parse_args()

    import logging
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level='INFO',
        )

    # compute the pages local variable,
    # which stores the pages to extract from wikipedia
    if args.page:
        output_prefix = f'wiki__page={args.page}'
        pages = [args.page]
    elif args.pages_file:
        import os
        output_prefix = f'wiki__pages_file={os.path.basename(args.pages_file)}'
        with open(args.pages_file, 'rt') as fin:
            pages = [line.strip() for line in fin.readlines()]
    else:
        print('must supply either --page or --pages_file')
        import sys
        sys.exit(1)
    
    # write the wikipedia contents to a file
    output_path = args.output_dir + '/' + output_prefix + f',recursive_depth={args.recursive_depth}'
    logging.info(f"output_path={output_path}")
    with open(output_path, 'wt') as f:
        for line in get_wikipedia_contents(pages, args.recursive_depth):
            f.write(line + '\n')
