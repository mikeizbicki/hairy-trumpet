#!/bin/python3

import copy
import re
import json
import os

titles = [
    'President',
    'Vice President',
    'Senator',
    'Governor',
    'Congressman',
    'Congresswoman',
    'Congressperson',
    'Honorable',
    'Justice',
    ]
titles = titles + ['Former ' + title for title in titles]
titles.sort(key=len, reverse=True)


def name_to_patterns(name):
    '''
    Given an input name, return a list of all possible strings that will be used to match that name.
    This is a helper function used to create the mask_patterns for the create_db function.

    >>> name_to_patterns('JD Vance')
    ['JD Vance', 'Vance']
    >>> name_to_patterns('Donald J. Trump')
    ['Donald J. Trump', 'Trump', 'Donald Trump']
    >>> name_to_patterns('Bob Casey Jr.')
    ['Bob Casey_Jr.', 'Casey_Jr.']
    >>> name_to_patterns('Donald Trump Jr.')
    ['Donald Trump_Jr.', 'Trump_Jr.']
    '''
    splits = name.split()
    if splits[-1][-1] == '.':
        name = ' '.join(splits[:-1]) + '_' + splits[-1]
    patterns = [name]
    splits = name.split()
    if len(splits) > 1:
        patterns.append(splits[-1])
    if len(splits) == 3:
        patterns.append(splits[0] + ' ' + splits[2])
    return patterns


sample_names = [
    'Joe Biden',
    'Kamala Harris',
    'Tim Walz',
    'Donald J. Trump',
    'JD Vance',
    'North_Dakota',
    'South_Dakota',
    'Bob Casey Jr.',
    'Donald Trump Jr.',
    ]
sample_patterns = [pattern for name in sample_names for pattern in name_to_patterns(name)]


def create_dp(text, mask_patterns=sample_patterns):
    '''
    Remove all examples of mask_patterns from the text and replace with mask tokens.

    >>> create_dp('Former president Donald Trump and vice president Kamala Harris are presidential candidates.')
    {'masked_text': 'Former president [MASK0] and vice president [MASK1] are presidential candidates.', 'masks': ['Donald Trump', 'Kamala Harris']}

    The following examples show how the common permutations of Trump and Harris's names get transformed.

    >>> create_dp('President Donald Trump')
    {'masked_text': 'President [MASK0]', 'masks': ['Donald Trump']}
    >>> create_dp('President Donald J. Trump')
    {'masked_text': 'President [MASK0]', 'masks': ['Donald J. Trump']}
    >>> create_dp('President Trump')
    {'masked_text': 'President [MASK0]', 'masks': ['Trump']}

    >>> create_dp('Vice President Kamala Harris')
    {'masked_text': 'Vice President [MASK0]', 'masks': ['Kamala Harris']}
    >>> create_dp('Vice President Harris')
    {'masked_text': 'Vice President [MASK0]', 'masks': ['Harris']}

    Titles do not get removed if they are not next to a person.

    >>> create_dp('The President is a person.')
    {'masked_text': 'The President is a person.', 'masks': []}
    >>> create_dp('The president is a person.')
    {'masked_text': 'The president is a person.', 'masks': []}

    The following examples test weird edge cases with capitalization and punctuation.

    >>> create_dp('hello Trump blah Donald Trump blah blah Harris')
    {'masked_text': 'hello [MASK0] blah [MASK1] blah blah [MASK2]', 'masks': ['Trump', 'Donald Trump', 'Harris']}
    >>> create_dp('Trump Trumpy, Trump. Trump! Trumpet TRUMPPPP trump TRUMP')
    {'masked_text': '[MASK0] Trumpy, [MASK1]. [MASK2]! Trumpet TRUMPPPP [MASK3] [MASK4]', 'masks': ['Trump', 'Trump', 'Trump', 'trump', 'TRUMP']}

    >>> create_dp('North Dakota is a state.')
    {'masked_text': '[MASK0] is a state.', 'masks': ['North_Dakota']}
    >>> create_dp('North Dakota and South Dakota are different states.')
    {'masked_text': '[MASK0] and [MASK1] are different states.', 'masks': ['North_Dakota', 'South_Dakota']}

    FIXME: 
    >>> create_dp('Trump Jr. and Trump are family.')
    {'masked_text': '[MASK0] and [MASK1] are family.', 'masks': ['Trump_Jr.', 'Trump']}
    >>> create_dp('thisisamadeupwordTrump should not match.')
    {'masked_text': 'thisisamadeupwordTrump should not match.', 'masks': []}
    '''
    mask_patterns = sorted(mask_patterns, key=len, reverse=True)
    regex = '|'.join([r'(?<=[^\w])' + mask_pattern.replace('_', ' ') + r'(?=[^\w]|$)' for mask_pattern in mask_patterns])
    text = ' ' + text
    masked_text = ''
    masks = []
    lastindex = 0
    for i, match in enumerate(re.finditer(regex, text, flags=re.IGNORECASE)):
        masked_text += text[lastindex:match.span()[0]]
        lastindex = match.span()[1]
        masked_text += f'[MASK{i}]'
        mask = match.group()
        mask_ = mask.replace(' ', '_')
        if mask_ in mask_patterns:
            mask = mask_
        masks.append(mask)
    masked_text += text[lastindex:]
    masked_text = masked_text[1:]
    return {'masked_text': masked_text, 'masks': masks}


def dp_rmtitles(dp):
    '''
    >>> dp_rmtitles({'masked_text': 'President [MASK0] and Senator [MASK1] are presidential candidates.', 'masks': ['Trump', 'Biden']})
    {'masked_text': '[MASK0] and [MASK1] are presidential candidates.', 'masks': ['Trump', 'Biden']}
    >>> dp_rmtitles({'masked_text': '[MASK0] is the current president.', 'masks': ['Biden']})
    {'masked_text': '[MASK0] is the current president.', 'masks': ['Biden']}
    >>> dp_rmtitles({'masked_text': 'Vice President [MASK0].', 'masks': ['Harris']})
    {'masked_text': '[MASK0].', 'masks': ['Harris']}
    '''
    masked_text = dp['masked_text']
    for title in titles:
        masked_text = masked_text.replace(f'{title} [', '[')
    return {'masked_text': masked_text, 'masks': dp['masks']}


def dp_split(dp):
    '''
    Given a single datapoint as input that (may) contain multiple masks,
    split that datapoint into one datapoint per mask.

    >>> dp_split({'masked_text': '[MASK0], [MASK1], [MASK0], [MASK1].', 'masks': ['Trump', 'Harris']})
    [{'masked_text': '[MASK0], Harris, [MASK0], Harris.', 'masks': ['Trump']}, {'masked_text': 'Trump, [MASK0], Trump, [MASK0].', 'masks': ['Harris']}]
    '''
    dps = []
    for i, imask in enumerate(dp['masks']):
        masked_text = dp['masked_text']
        for j, jmask in enumerate(dp['masks']):
            if i != j:
                masked_text = masked_text.replace(f'[MASK{j}]', jmask)
            if i == j:
                masked_text = masked_text.replace(f'[MASK{j}]', '[MASK0]')
        dps.append({'masked_text': masked_text, 'masks': [imask]})
    return dps


def dp_group(dp):
    '''
    If the same word has been masked multiple times in input text,
    we remove those duplicates.

    >>> dp_group({'masked_text': '[MASK0], [MASK1], [MASK2] are the same person.', 'masks': ['Trump', 'Trump', 'Trump']})
    {'masked_text': '[MASK0], [MASK0], [MASK0] are the same person.', 'masks': ['Trump']}
    >>> dp_group({'masked_text': '[MASK0], [MASK1], [MASK2], [MASK3].', 'masks': ['Trump', 'Harris', 'Trump', 'Harris']})
    {'masked_text': '[MASK0], [MASK1], [MASK0], [MASK1].', 'masks': ['Trump', 'Harris']}
    >>> dp_group({'masked_text': '[MASK0], [MASK1], [MASK2], [MASK3].', 'masks': ['Trump', 'Trump', 'Harris', 'Harris']})
    {'masked_text': '[MASK0], [MASK0], [MASK1], [MASK1].', 'masks': ['Trump', 'Harris']}
    '''
    found_masks = []
    masked_text = dp['masked_text']
    for i, mask in enumerate(dp['masks']):
        if mask not in found_masks:
            found_masks.append(mask)
        i_new = found_masks.index(mask)
        mask_str = f'[MASK{i}]'
        mask_loc = masked_text.find(mask_str)
        masked_text = masked_text[:mask_loc] + f'[MASK{i_new}]' + masked_text[mask_loc + len(mask_str):]
    return {'masked_text': masked_text, 'masks': found_masks}


def dp_canonicalize(dp):
    '''
    Ensures that different versions of the same label are converted into the same name.
    For example, both "Trump" and "Donald Trump" should have the label "Trump".

    >>> dp_canonicalize({'masked_text': '[MASK0], [MASK1], [MASK2] are the same person.', 'masks': ['Donald Trump', 'Trump', 'President Trump']})
    {'masked_text': '[MASK0], [MASK1], [MASK2] are the same person.', 'masks': ['Trump', 'Trump', 'Trump']}
    '''
    dp = copy.deepcopy(dp)
    for i, mask in enumerate(dp['masks']):
        dp['masks'][i] = mask.split()[-1].capitalize()
    return dp


def split_into_sentences(text):
    r''' 
    Split the input text into sentences.

    >>> split_into_sentences('This is a sentence. This is another sentence!  And another sentence.')
    ['This is a sentence.', 'This is another sentence!', ' And another sentence.']
    >>> split_into_sentences('Dr. Jones is a doctor.')
    ['Dr. Jones is a doctor.']
    >>> split_into_sentences('How much money? 1.5 million dollars.')
    ['How much money?', '1.5 million dollars.']
    >>> split_into_sentences('U.S.A. is a country. The U.N. is an international organization. I.B.M. is a tech company. Mr. Smith went to the store.')
    ['U.S.A. is a country.', 'The U.N. is an international organization.', 'I.B.M. is a tech company.', 'Mr. Smith went to the store.']
    >>> split_into_sentences('This is a sentence. "This is another sentence." This is a sentence.')
    ['This is a sentence.', '"This is another sentence."', 'This is a sentence.']
    >>> split_into_sentences('This is a sentence. "This is another sentence?" This is a sentence.')
    ['This is a sentence.', '"This is another sentence?"', 'This is a sentence.']
    '''
    sentence_end_pattern = r'(?<!\w\.\w\.)(?<!\b[A-Z][a-z]\.)(?<![A-Z]\.)(?<=\.|\?|\!|")\s|\\n'
    sentences = re.split(sentence_end_pattern, text)
    sentences = [sentence for sentence in sentences if sentence]
    return sentences


if __name__ == '__main__':

    valid_transformations = {name[3:]:f for name,f in locals().items() if name.startswith('dp_')}

    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file_to_mask')
    parser.add_argument('file_with_masks')
    parser.add_argument('--out_dir', default='data')
    parser.add_argument('--print_every', default=1, type=int)
    parser.add_argument('--minwords', default=10, type=int)
    parser.add_argument('--dpsize', choices=['sentence', 'paragraph'], default='paragraph')
    parser.add_argument('--transformations', nargs='*', default=['canonicalize', 'group', 'rmtitles', 'split'], choices=valid_transformations.keys())
    args = parser.parse_args()

    import logging
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level='INFO',
        )

    with open(args.file_with_masks) as fin:
        mask_patterns = [pattern for line in fin.readlines() for pattern in name_to_patterns(line.strip())]
        file_with_masks = os.path.basename(args.file_with_masks)

    with open(args.file_to_mask, 'rt') as fin:
        total_lines = len(list(fin))

    with open(args.file_to_mask, 'rt') as fin:
        output_file = args.out_dir + '/' + os.path.basename(args.file_to_mask)
        transformations_str = str(args.transformations).replace("'", "")
        output_file += f'__dpsize={args.dpsize},transformations={transformations_str}'
        with open(output_file, 'wt') as fout:
            for i, line in enumerate(fin):
                line = line.strip()
                if (i+1)%args.print_every == 0:
                    logging.info(f'procesing line {i}/{total_lines} = {100*i/total_lines:0.2f}%')
                if len(line) == 0 or line[0] == '=':
                    continue

                texts = [line]
                if args.dpsize == 'sentence':
                    texts = split_into_sentences(line)
                for text in texts:
                    if len(text.split()) < args.minwords:
                        continue
                    dp = create_dp(text, mask_patterns)
                    dps = [dp]
                    for transformation in args.transformations:
                        dps1 = []
                        for dp in dps:
                            dp1 = valid_transformations[transformation](dp)
                            if type(dp1) == list:
                                dps1 += dp1
                            else:
                                dps1.append(dp1)
                        dps = dps1

                    for dp in dps:
                        if len(dp['masks']) > 0:
                            fout.write(json.dumps(dp) + '\n')
