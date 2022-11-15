# ExplanationHardness

Supporting data for our EMNLP 2022 paper:

[Are Hard Examples also Harder to Explain? A Study with Human and Model-Generated Explanations](https://arxiv.org/abs/2211.07517)

[Swarnadeep Saha](https://swarnahub.github.io/), [Peter Hase](https://peterbhase.github.io/), [Nazneen Rajani](https://www.nazneenrajani.com/), and [Mohit Bansal](https://www.cs.unc.edu/~mbansal/)

## Data
We collect generalizable rule-based explanations for a subset of the [WinoGrande](https://arxiv.org/abs/1907.10641) dataset. All supporting data can be found inside the ```data``` folder. It consists of three folders: ```easy```, ```medium```, and ```hard```.

### Easy Samples

We collect human-written explanations for 500 easy samples, which are further divided into 100 test samples and 400 samples for retrieving in-context examples. These are present in ```easy/pool_400.tsv``` and ```easy/test_100.tsv``` respectively.

The GPT-3 generated explanations for the 100 test samples are present in ```gpt_generations.txt```.

### Hard Samples

Similarly, we also collect human-written explanations for 500 hard samples, which are further divided into 100 test samples and 400 samples for retrieving in-context examples. These are present in ```hard/pool_400.tsv``` and ```hard/test_100.tsv``` respectively.

The GPT-3 generated explanations for the 100 test samples are present in ```gpt_generations.txt```.

### Medium Samples

The human-written and GPT-3 generated explanations for 100 medium examples are present in ```medium/test_100.tsv``` and ```medium/gpt_generations.txt``` respectively.

## Computing Hardness of Samples for Winogrande

We compute hardness of samples using [Data Maps](https://aclanthology.org/2020.emnlp-main.746/) and use mean confidence to rank the samples. The easy and hard samples are the ones with the most and least confidence respectively. We thank the authors of Dataset Cartography for releasing their codebase [here](https://github.com/allenai/cartography).

## Generating Explanations using GPT-3

Use the script ```generate_gpt3_explanations.py``` to generate explanations via GPT-3 by filling in the OpenAI API key and other paths.

### Citation
```
@inproceedings{saha2022are,
  title={Are Hard Examples also Harder to Explain? A Study with Human and Model-Generated Explanations},
  author={Saha, Swarnadeep and Hase, Peter and Rajani, Nazneen and Bansal, Mohit},
  booktitle={EMNLP},
  year={2022}
}
```
