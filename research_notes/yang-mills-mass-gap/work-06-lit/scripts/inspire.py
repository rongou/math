import json, sys, urllib.request, urllib.parse, time
BASE = "https://inspirehep.net/api/"
FIELDS = "titles,abstracts,authors.full_name,publication_info,dois,arxiv_eprints,preprint_date"
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=40))
def show(md, full=True):
    t = (md.get("titles") or [{}])[0].get("title")
    au = [a["full_name"] for a in md.get("authors", [])][:8]
    pi = md.get("publication_info") or []
    pubs = []
    for p in pi:
        pubs.append("%s %s (%s) %s-%s" % (p.get("journal_title"), p.get("journal_volume"), p.get("year"), p.get("page_start"), p.get("page_end")))
    ax = [e.get("value") for e in md.get("arxiv_eprints", [])]
    dois = [d.get("value") for d in md.get("dois", [])]
    print("TITLE:", t)
    print("AUTHORS:", "; ".join(au))
    print("PUB:", " | ".join(pubs), "| DOI:", dois, "| arXiv:", ax, "| preprint_date:", md.get("preprint_date"))
    if full:
        for a in md.get("abstracts", [])[:1]:
            print("ABSTRACT:", a.get("value"))
    print("-----")
mode = sys.argv[1]
for arg in sys.argv[2:]:
    try:
        if mode == "doi":
            d = fetch(BASE + "doi/" + arg + "?fields=" + FIELDS)
            show(d["metadata"])
        elif mode == "arxiv":
            d = fetch(BASE + "arxiv/" + arg + "?fields=" + FIELDS)
            show(d["metadata"])
        elif mode == "q":
            d = fetch(BASE + "literature?size=8&sort=mostrecent&fields=" + FIELDS + "&q=" + urllib.parse.quote(arg))
            for h in d["hits"]["hits"]:
                show(h["metadata"], full=False)
        elif mode == "qa":
            d = fetch(BASE + "literature?size=8&sort=mostrecent&fields=" + FIELDS + "&q=" + urllib.parse.quote(arg))
            for h in d["hits"]["hits"]:
                show(h["metadata"], full=True)
    except Exception as e:
        print("ERR", arg, e); print("-----")
    time.sleep(1)
