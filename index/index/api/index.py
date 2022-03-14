"""Return comments on postid."""
import os
import re
import math
import flask
import index

# Initialize globals
page_ranks = {}
stopwords = []
big_dict = {}
norm_dict = {}


def get_initial_data():
    """Load initial data into memory."""
    print("Getting intial data.")
    # Get stopwords list
    print(os.getcwd())
    with open("index/index/stopwords.txt", "r") as docc:
        for line in docc.readlines():
            line = line.lower()
            line = line.rstrip()
            stopwords.append(line)

    # Get page rank dict
    with open("index/index/pagerank.out", "r") as docc:
        for line in docc.readlines():
            line = line.lower()
            line = line.rstrip()
            parts = line.split(',')
            page_ranks[parts[0]] = parts[1]

    # Make big dict
    with open("index/index/inverted_index.txt", "r") as docc:
        # For each  Term in Inverted index
        for line in docc.readlines():
            line = line.lower()
            line = line.rstrip()
            parts = line.split("\t")
            count = 0
            term = ""
            # For each value of one line of Inverted index

            docid = ""
            for word in parts:
                if count == 0:
                    term = word.strip()
                    if term not in big_dict:
                        big_dict[term] = {}
                        big_dict[term]["docs"] = {}

                # Second word (idf)
                elif count == 1:
                    big_dict[term]["idf"] = word.strip()

                # Doc ID
                elif count % 3 == 2:
                    docid = word.strip()
                    # print(docid)
                    # print("docid: ", docid)
                    big_dict[term]["docs"][docid] = {}

                # Frequency in doc
                elif count % 3 == 0:
                    big_dict[term]["docs"][docid]["freq"] = word.strip()

                # Normalization Factor
                elif count % 3 == 1:
                    big_dict[term]["docs"][docid]["norm"] = word.strip()
                    norm_dict[docid] = word.strip()

                count += 1
        # print("length of the big dict now: ", len(big_dict))
        # print(json.dumps(big_dict, indent=4))
        # print(num1)


@index.app.route('/api/v1/',
                 methods=['GET'])
def get_smth():
    """Get Hits."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


def get_query_list(query_list, query):
    """Get query list."""
    for word in query:
        word = re.sub(r'[^a-zA-Z0-9]+', '', word)
        word = word.lower()
        word = word.rstrip()
        if word not in stopwords:
            query_list.append(word)
    return query_list


def get_doc_list(temp_list, word):
    """Get a certain list of docs."""
    for num1 in big_dict[word]["docs"].keys():
        temp_list.append(num1)
    return temp_list


@index.app.route('/api/v1/hits/',
                 methods=['GET'])
def get_results():
    """Get Hits."""
    weight = float(flask.request.args.get("w", default=1, type=str))
    query = flask.request.args.get("q", default="", type=str)
    query = query.split()
    query_list = []
    query_list = get_query_list(query_list, query)
    nice_list = []

    # print("query list is ", query_list)
    for word in query_list:
        temp_list = []
        # If non existent
        if word not in big_dict.keys():
            return {"hits": []}

        # Make list of docs that contain word
        temp_list = get_doc_list(temp_list, word)
        # Append list to list of lists
        nice_list.append(temp_list)

    # Make list of Docs containing all query words
    if len(nice_list) == 0:
        return {"hits": []}

    temp_list = nice_list[0]
    for word in nice_list:
        # print("current list:", temp_list)
        temp_list = set(word) & set(temp_list)

    if temp_list == []:
        # END - NO RESULTS FOUND
        return {"hits": []}

    # print("temp_list after intersection: ", temp_list)
    # If no Document contains all words

    query = []
    d_vector = {}

    # Count the freqs of terms in query
    small_dict = {}
    for word in query_list:
        if word in small_dict.keys():
            small_dict[word] += 1
        else:
            small_dict[word] = 1

    # Calculate the norm factor for the query
    norm_sum = 0
    for word in query_list:
        query.append(small_dict[word] * big_dict[word]["idf"])
        num1 = math.pow(float(big_dict[word]["idf"]), 2)
        num2 = math.pow(float(small_dict[word]), 2)
        norm_sum += num1 * num2

    norm_sum = math.sqrt(norm_sum)
    # Make document vector for each doc
    # wtf happened here

    # if len(temp_list) == 0:
    # return {"hits": []}

    for docid in temp_list:
        temp_list_1 = []
        for word in query_list:
            temp_list_1.append(float(big_dict[word]["idf"]) *
                               float(big_dict[word]["docs"][docid]["freq"]))
        # Add docs d_vec to dict of vecs
        d_vector[docid] = temp_list_1

    small_dict = {}
    small_dict["hits"] = []

    for word in d_vector:
        temp_dict = {}
        temp_dict["docid"] = int(word)
        zippy = zip(d_vector[word], query)
        num1 = sum(float(i[0]) * float(i[1]) for i in zippy)
        num1 = num1/(float(norm_sum) * math.sqrt(float(norm_dict[word])))
        num2 = float(page_ranks[word])
        temp_dict["score"] = (1 - weight) * num1 + weight * num2
        small_dict["hits"].append(temp_dict)

    # context = json.dumps(small_dict)
    small_dict["hits"] = sorted(small_dict["hits"],
                                key=lambda i: i['score'],
                                reverse=True)
    # print(small_dict)
    return flask.jsonify(**small_dict)
