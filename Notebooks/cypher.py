def encode (title, body):

    # Import dependancies
    import pandas as pd
    import numpy as np
    from nltk.tokenize import RegexpTokenizer
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords

    # Define the coded list
    coded = [1]

    # Set up the tokenizer
    index_df = pd.read_csv('word_index.csv', index_col=0)
    tokenizer = RegexpTokenizer(r'\w+')
    results = tokenizer.tokenize(title)
    stop_words = set(stopwords.words('english'))

    # Tokenize the title
    for word in results:
        word = word.lower()
    if word not in stop_words:
        try:
            coded.append(index_df.loc[word].values[0])
        except:
            coded.append(3)
    
    # Tokenkize the body
    coded.append(2)
    results = tokenizer.tokenize(body)
    for word in results:
        word = word.lower()
        if word not in stop_words:
            try:
                coded.append(index_df.loc[word].values[0])
            except:
                coded.append(3)
    return coded

def decode(coded):
    import pandas as pd
    import numpy as np
    from nltk.tokenize import RegexpTokenizer
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords

    # Set up tokenizer
    decoded = []
    index_df = pd.read_csv('word_index.csv', index_col=0)
    index_df.reset_index(inplace=True)
    index_df.set_index('0', inplace=True)
    decoded.append('<TITLE>')

    # Decode List
    for word in coded[2:]:
        decoded.append(index_df.loc[word].values[0])

    return decode
