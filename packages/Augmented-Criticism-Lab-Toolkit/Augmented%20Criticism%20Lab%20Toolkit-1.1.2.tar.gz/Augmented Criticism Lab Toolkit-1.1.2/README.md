# Augmented Criticism Lab Toolkit and Connectors

This set of tools is designed for interfacing with the Augmented Criticism Lab's API, 
[https://acriticismlab.org](https://api.acriticismlab.org). The toolkit can be installed with pip:

```
pip install Augmented-Criticism-Lab-Toolkit
```

## Using the Connectors

Connectors are used to pull data from the database over the API. Here are some examples:

```python
from connectors.poem import Poem

# To get a list of all poems:
all_poems = Poem().all()

# To get a specific poem by database id:
single_poem = Poem().by_id(1)

from connectors.book import Book

# To get a list of all books:
all_books = Book().all()

# To get a specific book by database id:
single_book = Book().by_id(1)
```

The included connectors are book, poem, section, and tools. Each connector works on the same principle.

## Using the Tools

### API based tools:

```python
from tools.api import Tools
# Lemmatize text:
lemmas = Tools().lemmatize("text to lemmatize")

# Part of speech tags:
tags = Tools().pos_tag("text to tag")

# Frequency distribution:
freqdist = Tools().frequency_distribution("text to get distribution for")

# Topic model:
model = Tools().topic_model("text to model")
```

**Note:** Topic models take about a minute to run.

### Python based tools:

**Rhyme Scheme Analyzer:**

```python
from tools.rhyme import Rhyme
from tools.rhyme import classify_sonnet

# Initialize a Rhyme object with the text you want to analyze.
# The text must be separated into lines, you can define a delimiter
# the default is '\\n'. This returns a list of rhyme pairs:
# ['A','B','B','A','C','D','D','C','E','F','E','F','G,'G']
rhyme = Rhyme("text\n broken\n into lines", delimiter='\n').find_rhyme_scheme()

# To classify the rhyme scheme (only works for sonnets) run:
# Returns a tuple such that (each number represents a probability
# the sonnet of the type listed):
#(Petrarchan 1, Petrarchan 2, Petrarchan 3, Shakespearian,  Spenserian)
sonnet_type = classify_sonnet(rhyme)
```

**Syllable Counter:**

```python
from tools.syllable import SyllableCounter

# Initialize a counter:
syllable_counter = SyllableCounter()

# Run a line of poetry through the counter:
syllable_count_for_line = syllable_counter.count_syllables_by_line("line of text")
```



