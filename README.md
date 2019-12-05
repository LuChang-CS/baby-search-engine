# baby-search-engine
A baby search engine for CS600 course project using compressed trie and django.

## Summary
We use a compressed trie to index the words appearing in the html files. We also store the occurrence list of each word as an independant file to the disk. In this list, we store the link's id and the frenquency of the word in this html. When searching using the engine, we first use the compressed trie to search the index of the given words and find the occurrence list on the disk. Finally we return the title and link that contains the given words.

## Requirements
- Python 3
- bs4
- goose3
- nltk
- django
- requests

## Instructions
1. Install all required softwares and packages
```bash
pip install -r requirements.txt
```
2. In the python console, download the `stopwords` and `punkt` corpus required by `nltk`
```python
import nltk


nltk.download('stopwords')
nltk.download('punkt')
```
3. Run `preprocess.py` to download html files, extract information and construct trie:
```bash
python preprocess.py
```
4. Run the django server in your terminal, open your browser and type [`localhost:8000`](http://localhost:8000):
```bash
python ./main.py runserver 0.0.0.0:8000
```
5. Type some words to examine the search results, like 'election', 'debate' and 'minister' etc.

<img width="45%" src="https://raw.githubusercontent.com/LuChang-CS/baby-search-engine/master/screenshots/1.png" />
<img width="45%" src="https://raw.githubusercontent.com/LuChang-CS/baby-search-engine/master/screenshots/2.png" />

## Notes
1. If you input empty text, the system will jump back to the index page.
2. We will remove the english stopwords in the query text input.
3. We limit the query text with 64 characters.
4. You can use space and punctuations to split the input words.
5. We will stem the input words to search the results.

## Algoithms and Data Structures

### Compressed Trie
We use a compressed trie as described in out textbook to store the words and their indexes.
- **Inserting** &nbsp;&nbsp;&nbsp;&nbsp; We directly inserting words to the compressed trie. When inserting a word, we compare the current word with the key of the node and find the common prefix. Then we recursively do this operation to the end of this word. Finally we store the value of this word to the external node. A trick is we use a space as the key of external nodes so that we don't require a word not being the prefix of other words.
- **Searching** &nbsp;&nbsp;&nbsp;&nbsp; Searching is similiar to inserting. But we need a perfect match of key and current word. We only claim the word exists in the trie until we find an external node with the key of space. Finally, we return the value of this word.

All time complexites are the same as those in our textbook.

### Occurrence List
A problem is how to match the word with it's occurence. My solution in this baby search engine is we store the id of the word in the trie, and store the occurence list to the disk, of which the filename is the same as thw word id.

An occurence list consists of the link id which this word appears in, the term frequency of this word in each link and a score of each link corresponding to this word.
```bash
[
    [link_id, frequency, score],
    [link_id, frequency, score],
    ...
]
```

### Ranking
In this baby engine, we use the combination of the frequency of a word and the page rank to evaluate each link to the given word. More specifically, the final score $s_{wi}$ of link $i$ to the word $w$ is
$$ s_{wi} = f_{wi} \times r_i $$
where $f_{wi}$ is the term frequency of $w$ in link $i$, and $r_i$ is the page rank of link $i$. (See [PageRank - Wikiedia](https://en.wikipedia.org/wiki/PageRank))

### Preprocess
The input of `preprocess.py` is a url file located in `data/input/urls`. Our program will automatically download the html file and extract the title, links contained in html and pure content of html. Then it will insert all words to the compressed trie and update each occurence list. Finally, it will calculate the score and save the trie to the disk.
