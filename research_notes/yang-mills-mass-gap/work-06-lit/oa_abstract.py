import json, sys, urllib.request, urllib.parse
def get(doi):
    url = "https://api.openalex.org/works/https://doi.org/" + doi
    req = urllib.request.Request(url, headers={"User-Agent": "mailto:research@example.org"})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=30))
    except Exception as e:
        return doi, "ERR " + str(e), None, None
    inv = d.get("abstract_inverted_index")
    abstract = None
    if inv:
        pos = {}
        for w, ps in inv.items():
            for p in ps:
                pos[p] = w
        abstract = " ".join(pos[i] for i in sorted(pos))
    return doi, d.get("title"), d.get("publication_year"), abstract
for doi in sys.argv[1:]:
    doi_, t, y, a = get(doi)
    print("DOI:", doi_)
    print("TITLE:", t, "| YEAR:", y)
    print("ABSTRACT:", a)
    print("-----")
