# GUI Word2Vec

This project is a simple GTK3 graphical user interface (GUI) for [gensim's Word2Vec](https://radimrehurek.com/gensim/). It's purpose is to streamline (at least a bit) the process of querying a W2V model. Currently, it only outputs the cosine similarity between inputed terms.

## How it works
It a __3__ step process:
1. Enter the words you want to use in the input field, each on a new line
2. Load the model, and wait a bit. The model must be a KeyedVectors Word2Vec `.wv` file 3. Query

The results will be a CSV file in the `exports`. The filename of the export is of the following format: `<year><month><day>_<hour><minute><second> - W2V_Cosines.csv`

An additional step for this application to work properly is to create a model that you can query. This app does not come with one by default for several reasons:
1. If you want proper results you need a corpus with at least [~10 million words](https://arxiv.org/abs/1610.01520) (else, use [LSA](https://en.wikipedia.org/wiki/Latent_semantic_analysis)). Which leads to point number...
2. Such a corpus typically has over 100 MB in size; this violates GitHub's file limit

## :exclamation: Prerequisites :exclamation:
Besides dependencies, you need a model. If you don't have one yet, then [make one](https://rare-technologies.com/word2vec-tutorial/) (make sure you save it as [KeyedVectors](https://radimrehurek.com/gensim/models/keyedvectors.html)). I also have a script [here](https://github.com/tudorpaisa/train-word2vec) to help you create your W2V model

## Dependencies
```
python3 gensim pandas scipy numpy pygobject3
```

## TODO
- [ ] Add a "Select model" button (to replace the model overwrite workaround)
- [ ] Add the entire palette of W2V querying options
- [ ] Make the model loading process run on a separate thread
- [ ] Consider a new naming scheme for the exports; _seconds might be a little bit overkill_

