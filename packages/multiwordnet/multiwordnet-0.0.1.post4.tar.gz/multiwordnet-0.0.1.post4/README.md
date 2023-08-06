### Background
A WordNet is a lexico-conceptual database for a language. In a WordNet, a language's lexemes (nouns, verbs, adjectives, and adverbs) are grouped into sets of semantically related words called synsets (for "synonym sets"), which thus correspond to the senses that are lexicalized in the language. A WordNet also typically includes information about semantic relations (i.e., relations between synsets) and about lexical relations (i.e., relations between words).

Created by Stefano Minozzi between 2004 and 2008 as part of the Fondazione Bruno Kessler's MultiWordNet, the original Latin WordNet contained 9,124 lemmas drawn from Riganti's Lessico Fondamentale Latino. The University of Exeter's TExtual Project aims to build on and expand Minozzi's work by adding some 30,000 words, covering the Latin language from the archaic period to late antiquity (and somewhat beyond).

When completed, this Latin WordNet '2.0' will become an integral component of two Digital Humanities projects. For the TExtual semantic and syntactic search engine for electronic corpora of Latin, the WordNet will deliver the engine's ability to execute queries based on word meanings. The WordNet will also provide the Exeter Dictionary of Latin Metaphor (Lexicon Translaticium Latinum) with a basis for distinguishing between words' literal and abstract senses.

### Installation
To get setup, all you need to do is compile the relevant SQLite databases:
```
>>> from multiwordnet.db import compile
>>> compile('latin')
```
You will need to do the same for the English and Italian synset databases:
```
>>> compile('english', 'synset)
>>> compile('italian', 'synset)
```
To make full use of the semantic data that is included in the MultiWordNet, you will also want to compile the list of common relations and semfield hierarchy:
```
>>> compile('common', 'relations', 'semfield', 'semfield_hierarchy')
```

### Basic usage
```
>>> from multiwordnet.wordnet import WordNet

>>> LWN = WordNet('latin')
>>> LWN.lemmas  # all the lemmas currently in the WordNet
...
>>> abalieno = LWN.get_lemma('abalieno', 'v')  # this returns a single lemma
>>> words = LWN.get('alien', strict=False)  # this returns possibly multiple lemmas matching a wildcard string
>>> for word in words:
...    print(word.lemma, word.pos)
...
alienus n
alieno v
alienigena n
alienatio n
abalieno v
abalienatio n
>>> abalieno.synonyms  # all lemmas that share a synset with 'abalieno'
>>> abalieno.antonyms
>>> abalieno.synsets
...

>>> synset = LWN.get_synset('n#07462736')  # you can find a synset directly, if you know its offset ID
>>> synset.lemmas
...