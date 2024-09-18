# Hairy Trumpet

<img align=right width=300px src=img/hairy-trumpet.jpg />

Hairy_Trumpet is a tool for generating [cloze style benchmarks](https://en.wikipedia.org/wiki/Cloze_test) for LLMs.
The benchmarks are designed to test the LLMs knowledge of a specific domain, and are not general purpose benchmarks.
This README file explains two examples from the mycology and politics domains,
although the tool can be used to generate benchmarks for any domain.
The resulting benchmarks are particularly useful for evaluating RAG-based systems.

## Structure of the data

A number of pre-made datasets are available in the [data](/data) subfolder.
Each dataset is contained in an individual `.jsonl` file,
with one line per datapoint.

An example data point from a mycology dataset looks like
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

<!--
## Generating new datasets

To generate a new dataset

The [Hairy Trumpet](https://en.wikipedia.org/wiki/Panus_fasciatus) is a type of fungus.
It is also the name of this tool for creating datasets about the Harris/Trump 2024 election.
-->
