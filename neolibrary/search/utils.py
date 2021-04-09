from string import ascii_lowercase as alpha


def str_to_regexp(str):
    regexp = str.replace('a', '[aâă]')\
                .replace('A', '[AÂĂ]')\
                .replace('t', '[tț]')\
                .replace('T', '[TȚ]')\
                .replace('s', '[sș]')\
                .replace('S', '[SȘ]')\
                .replace('i', '[iȋ]')\
                .replace('I', '[IȊ]')
    regexp = "(?i).*" + regexp + ".*"
    return regexp


def run_advanced_search(graph, ls, lim=None):
    '''
    ls - list of [LABEL, regexp_string]
    LABEL - one of "Book", "Author", "Tag"
    return - string that is a valid cypher query

    Constructs an AND query like:
        match (b:Book)
        where b.name =~ $b[0]
        with b  // AND
        match (t:Tag)-[:TAGS]->(b)
        where t.name =~ $t[0]
        with b  // AND
        match (t:Tag)-[:TAGS]->(b)
        where t.name =~ $t[1]
        return b limit $lim
    '''
    query = ""
    for index, (label, regexp) in enumerate(ls):
        if label == "Book":
            query += ("match (b:Book) where b.name=~${}"\
                      +" with b \n").format(alpha[index])
        elif label == "Author":
            query += ("match (a:Author)-[:WROTE]->(b:Book)"\
                      +" where a.name=~${}"\
                      +" with b \n").format(alpha[index])
        elif label == "Tag":
            query += ("match (t:Tag)-[:TAGS]->(b:Book)"\
                      +" where t.name=~${}"\
                      +" with b \n").format(alpha[index])
    query += "return b\n"
    if lim:
         query += "limit $lim"
    args = {letter: regexp for (letter,(label, regexp)) in zip(alpha, ls)}
    dt = graph.run(query, args, lim=lim)

    return dt
