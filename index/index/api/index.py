"""Return comments on postid."""
import flask
import index

page_ranks = {}
stopwords = []
big_dict = {}

def get_initial_data():
    """Load initial data into memory."""
        
    # On Startup:
    #  Load inverted index, pagerank, and stopword files into mem.

    # Get stopwords list
    with open("stopwords.txt", "r") as docc:
        for line in docc.readlines():
            line = line.lower()
            line = line.rstrip()
            stopwords.append(line)

    # Get page rank dict
    with open("pagerank.out", "r") as docc:
        for line in docc.readlines():
            line = line.lower()
            line = line.rstrip()
            parts = line.split(',')
            page_ranks[parts[0]] = parts[1]

    # Make big dict
    with open("inverted_index_small.txt", "r") as docc:
        # For each  Term in Inverted index
        for line in docc.readlines():
            line = line.lower()
            line = line.rstrip()
            parts = line.split()
            count = 0
            term = ""
            
            # For each value of one line of Inverted index
            for word in parts:
                docid = ""
                # First word (term)
                if count == 0:
                    term = word
                    if not big_dict[term]:
                        big_dict[term] = {}

                # Second word (idf)
                elif count == 1:
                    idf = word
                    big_dict[term]["idf"] =  idf

                # Doc ID
                elif count % 3 == 2:
                    docid = word
                    big_dict[term]["docs"][docid] = {}

                # Frequency in doc
                elif count % 3 == 0:
                    freq = word
                    big_dict[term]["docs"][docid]["freq"] = freq
                    
                # Normalization Factor
                elif count % 3 == 1:
                    norm = word
                    big_dict[term]["docs"][docid]["norm"] = norm 
                    
                count += 1


@index.app.route('/api/v1/',
                    methods=['GET', 'POST'])
def get_smth():
    """Get Hits."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    
    return flask.jsonify(**context)

@index.app.route('/api/v1/hits/?w=<w>&q=<query>',
                    methods=['GET', 'POST'])
def get_results(postid_url_slug):
    """Get Hits."""

    weight = flask.request.args.get("w", default=1, type=int)
    query = flask.request.args.get("query", default="", type=str)

    query_list = query.split()
    # norm factor for query

    nice_list = []

    # For each word
    for word in query_list:
        temp_list = []
        # If non existent
        if word not in big_dict:
            # END - NO RESULTS FOUND
            return
        
        # Make list of docs that contain word
        for key in big_dict[word]["docs"]:
            temp_list.append(key)
            
        # Append list to list of lists
        nice_list.append(temp_list)

    # Make list of Docs containing all query words
    temp_list = nice_list[0]
    for elem in nice_list:
        temp_list = elem & temp_list
    
    # If no Document contains all words
    if temp_list == []:
        # END - NO RESULTS FOUND
        return

    q_vector = []
    d_vector = {}

    # Count the freqs of terms in query
    small_dict = {}
    for word in query_list:
        if small_dict[word]:
            small_dict[word] += 1
        else:
            small_dict[word] = 1

    # Calculate the norm factor for the query
    norm_sum = 0
    for word in query_list:
        q_vector.append(small_dict[word] * big_dict[word]["idf"])
        norm_sum += math.pow(float(big_dict[word]["idf"]), 2) * math.pow(float(small_dict[word]), 2)

    # Make document vector for each doc
    for docid in temp_list:
        temp_list = []
        for word in query_list:
            temp_list.append(big_dict[word]["idf"] * big_dict[word]["docs"][docid]["freq"])
        # Add docs d_vec to dict of vecs
        d_vector[docid] = temp_list
    
    results = {}
    results["hits"] = []
    
    for docid in d_vector:
        temp_dict = {}
        temp_dict[docid] = vec
        temp_dict["score"] = sum(i[0] * i[1] for i in zip(vec, q_vector))
        results["hits"].append(temp_dict)
    
    context = json.dumps(results)

    return flask.jsonify(**context)
    

# OH questions:
    # Confirm where parts connect with each other
    # Do we use inverted index from the first stage
    # Setup pls
    #   init.py
    #   config.py
    # 2nd route url 
    # When/Where to load pageRank into dict - call api/v1 on startup + load into global dictionary at top?