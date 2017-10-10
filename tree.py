from ete3 import Tree, TreeStyle, NodeStyle, faces, AttrFace, TreeFace
import itertools

# form of return is
# {'stem' : #stem_name,
#  'total_occurances' : #total,
#  'instances' : { 'abandon' : [num_occur, percent], 'abandoned' : [num_occur, percent]}
# }
def get_data_from_stem(word):
        data = {}
        infile =  "browncorpus_stemtowords_2.txt"
        with open (infile, "r" ) as infile:
                for line in infile:
                        items = line.split()
                        if len(items) == 0 or line[0] == '-':
                                continue
                        if not (items[0] == word):
                                continue
                        data['stem'] = items[0]
                        data['total_occurances'] = int(items[1])
                        data['instances'] = dict()
                        num_stems = (len(items) - 3) / 3
                        for i in range(num_stems):
                                new_word = items[(i + 1) * 3]
                                num_occur = int(items[(i + 1) * 3 + 1])
                                percent = float(items[(i + 1) * 3 + 2][:-1]) / 100.0
                                data['instances'][new_word] = [num_occur, percent]
                return data

def get_words_from_stem(word):
        data = []
        infile = "browncorpus_Signatures.txt"
        with open (infile, "r") as infile:
                found = False
                for line in infile:
                        if not (found):
                                if line[0] == '=' and line.split()[1] == word:
                                        found = True
                        else:
                                if len(line) == 0:
                                        continue
                                else:
                                        if line[0] == '-':
                                                return data
                                        else:
                                                words = line.split()
                                                for i in words:
                                                        data.append(i)
                return data

def get_words_data_from_suffix(word):
        data = {}
        list_stems = get_words_from_stem(word)
        if len(list_stems) == 0:
                return 0
        for stem in list_stems:
                word_data = get_data_from_stem(stem)
                data[word_data['stem']] = word_data
        return data

def get_sub_suffixes_words(word):
        suffixes = word.split('-')
        combinations = []
        for i in range(len(suffixes)):
                n = itertools.combinations(suffixes, i)
                for j in n:
                        if 'NULL' in j:
                                j[0], j[j.index['NULL']] = 'NULL', j[0]
                                j = j[0] + j[1:].sort()
                        combinations.append(j)
        return combinations

#generates ETE tree of words with suffixes
def makeETEtree(word, tree):
        suffixes = word.split('-')
        if len(suffixes) == 1:
                return
        else:
                combinations = itertools.combinations(suffixes, len(suffixes) - 1)
                for j in combinations:
                        j = list(j)
                        if 'NULL' in j and not(len(j) == 1):
                                j[0], j[j.index('NULL')] = 'NULL', j[0]
                                if len(j) > 2:
                                        j[1:].sort()
                        if len(j) == 1:
                                continue
                        child = tree.add_child(name = '-'.join(j))
                        makeETEtree('-'.join(j), child)

def makeETEWordsTree(word):
        t = Tree(name = word)
        list_words_data = get_words_data_from_suffix(word)
        if list_words_data == 0:
                t.name = '0'
                return t
        for i in list_words_data:
                child = t.add_child(name = i)
        return t
        # combinations = []
        # n = suffixes.combinations(len(suffixes) - 1)

        # list_suffixes_with_words = get_sub_suffixes_words(word)

ts = TreeStyle();

small_ts = TreeStyle()
small_ts.show_leaf_name = True
small_ts.scale = 100
small_ts.mode = "c"
ts.mode = "c"

def layout(node):
    if node.is_root():
        N = AttrFace("name", fsize=75, fgcolor="black")
    else:
        N = AttrFace("name", fsize=50, fgcolor="black")
    faces.add_face_to_node(N, node, 0)
    t = makeETEWordsTree(node.name)
    T = TreeFace(t, small_ts)
    # Let's make the sphere transparent
    T.opacity = 0.8
    # And place as a float face over the tree
    faces.add_face_to_node(T, node, 1)

def makeETESuffixTree(word):
        t = Tree(name = word)
        ts.show_leaf_name = False
        ts.layout_fn = layout
        makeETEtree(word, t)
        for l in t.get_leaves():
                if makeETEWordsTree(l.name).name == '0':
                        print l
                        l.delete()
        t.show(tree_style = ts)
