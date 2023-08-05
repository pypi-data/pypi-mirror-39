import gzip, pickle
import ahocorasick

def read(wiki_titles):
    with gzip.open(wiki_titles, "rt", encoding="utf-8") as fr:
        for i, line in enumerate(fr):
            yield line.strip()
            if i > 1000000:
                break

def create_automaton(wiki_titles):
    a = ahocorasick.Automaton()

    for i, line in enumerate(read(wiki_titles)):
        a.add_word(line.lower(), i)
    a.make_automaton()

    return a

if __name__ == "__main__":

    # https://dumps.wikimedia.org/enwiki/20180701/enwiki-20180701-all-titles-in-ns0.gz
    wiki_path = "enwiki-latest-all-titles-in-ns0.gz"
    pickle_path = "/mnt/ext1/programming/enwiki.p"

    if True:
        with open(pickle_path, "wb") as fw:
            a = create_automaton(wiki_path)
            pickle.dump(a, fw)
            del a

    with open(pickle_path, "rb") as fr:
        a = pickle.load(fr)
