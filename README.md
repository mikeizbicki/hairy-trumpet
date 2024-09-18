# Hairy Trumpet

<img align=right width=300px src=img/hairy-trumpet.jpg />

Hairy_Trumpet is a tool for generating [cloze style benchmarks](https://en.wikipedia.org/wiki/Cloze_test) for LLMs.
These benchmarks are designed to be *domain specific* and not general purpose benchmarks.
This README file explains two examples from the mycology and politics domains,
although the tool can be used to generate benchmarks for any domain.
The resulting benchmarks are particularly useful for evaluating the effectiveness of RAG-based systems.

## Structure of the data

A number of pre-made datasets are available in the [data](/data) subfolder.
Each dataset is contained in an individual `.jsonl` file.

An example data point from the mycology data looks like
```
{
    "masked_text": "Panus fasciatus (common name includes [MASK0]) is a species of fungus in the family Polyporaceae in the genus Panus of the Basidiomycota.",
    "masks": ["Hairy_trumpet"]
}
```
The task is:
Given the `masked_text` portion of a data point,
predict the `masks` portion of the data point.

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
