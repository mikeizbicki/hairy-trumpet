# Hairy Trumpet

<img align=right width=200px src=img/hairy-trumpet.jpg />

Hairy Trumpet is a tool for generating [cloze style benchmarks](https://en.wikipedia.org/wiki/Cloze_test) for LLMs.
The benchmarks are designed to test the LLMs domain-specific knowledge, and are not general purpose benchmarks.
It is particularly useful for evaluating RAG systems.
<!--
The tool was originally designed for generating datasets related to the US 2024 presidential election cycle,
but can be used to generate benchmarks for arbitrary domains.
-->

**Example 1:**
A dataset designed to evaluate an LLM's knowledge of fungus could have a data point like
<!--
The fungus species panus fasciatus has common name [MASK0].
-->
```
Panus fasciatus (common name includes [MASK0]) is a species of fungus in the family Polyporaceae in the genus Panus of the Basidiomycota.
```
The goal of the LLM would be to predict the value of `[MASK0]`,
which in this case should be `hairy trumpet`.
In order to correctly predict this value,
the LLM clearly needs to know the relationship between common and scientific names for this fungus species.

<img align=right width=200px src=img/harris-trump.jpg />

**Example 2:**
A different dataset designed to evaluate an LLM's knowledge of the US 2024 election might have a data point like
```
[MASK0] is the democratic presidential nominee, and [MASK1] is the republican nominee.
```
Here, the model must correctly guess that `[MASK0]` refers to `Harris` and `[MASK1]` corresponds to `Trump`.
This is a challenging task for an LLM because the election news is outside of the training data for all current LLMs,
and therefore a RAG-type system is required for them to acquire this knowledge.


## Structure of the data

A number of pre-made datasets are available in the [data](/data) subfolder.
Each dataset is contained in an individual [JSONL file](https://jsonlines.org/).
That is, every data point is a JSON object,
and every line is one data point.

The following code block shows a (pretty printed) example data point.
```
{
    "masked_text": "Panus fasciatus (common name includes [MASK0]) is a species of fungus in the family Polyporaceae in the genus Panus of the Basidiomycota.",
    "masks": ["Hairy_trumpet"]
}
```
The task is:
Given the `masked_text`,
predict the `masks`.
Valid values for the `masks` are contained in the file `masks/mycology`:
```
$ cat masks/mycology
hairy_trumpet
panus_fasciatus
candy_cap
truffle
jelly_fungi
```
In this case, there are a small number of possible masks,
each of which is a different species of fungus.
This task is therefore equivalent to a multiple-choice question evaluating the model's knowledge of these fungus species.

Data points are allowed to have multiple masked words,
such as in the following example from the politics domain.
```
{
    "masked_text": "[MASK0] is the democratic presidential nominee, and [MASK1] is the republican nominee.",
    "masks": ["Harris", "Trump"]
}
```
Being able to correctly predict the masks in the masked text demonstrates that a model understands the concept of the "masked out" word(s).
## Generating Datasets

Generating new datasets is a 3 step process.

**Step 1: Defining the domain.**

The first step to generating a dataset is to define the domain of knowledge.
These are stored as individual files in the `domains` subfolder.
Each line of the file contains a single topic that will be a keyword masked from the domain.
For example, the file `domains/mycology` contains a variety of fungus names.
```
$ cat domains/mycology
hairy_trumpet
panus_fasciatus
candy_cap
truffle
jelly_fungi
```
The file `domains/election2024` contains the names of presidential candidates (from major and minor parties) in the 2024 US presidential election.
```
$ cat domains/election2024
Joe Biden
Kamala Harris
Tim Walz
Donald Trump
JD Vance
Chase Oliver
Mike ter Maat
Jill Stein
Butch Ware
```

**Step 2: Generating Ground Truth.**

The file `scripts/download_wiki.py` can be used to download high quality sentences from wikipedia.
For example:
```
$ python3 scripts/download_wiki.py --domain_file=domains/mycology
$ python3 scripts/download_wiki.py --domain_file=domains/election2024
```
This script will search wikipedia for all pages related to the keywords in the specified `--domain_file` and download those pages into a single file in the `raw` directory.

The script `tests/download_wiki.sh` contains more examples.

**Step 3: Generating Masks:**

The final step is to use `scripts/apply_mask.py` to "mask out" the appropriate keywords in the ground truth file.
The script `tests/apply_mask.sh` shows example usage.


<!--
## Generating new datasets

To generate a new dataset

The [Hairy Trumpet](https://en.wikipedia.org/wiki/Panus_fasciatus) is a type of fungus.
It is also the name of this tool for creating datasets about the Harris/Trump 2024 election.
-->
