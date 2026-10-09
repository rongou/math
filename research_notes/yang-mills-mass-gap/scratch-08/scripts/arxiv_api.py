import sys, urllib.request, urllib.parse, time
import xml.etree.ElementTree as ET
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
def q(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research-script"})
    return urllib.request.urlopen(req, timeout=60).read()
def show(entry, full=True):
    g = lambda tag: (entry.find(tag, NS).text or "").strip() if entry.find(tag, NS) is not None else ""
    aid = g("a:id").split("/abs/")[-1]
    title = " ".join(g("a:title").split())
    authors = [a.find("a:name", NS).text for a in entry.findall("a:author", NS)]
    jr = entry.find("arxiv:journal_ref", NS)
    doi = entry.find("arxiv:doi", NS)
    cats = [c.get("term") for c in entry.findall("a:category", NS)]
    print("ID:", aid, "| published:", g("a:published")[:10], "| updated:", g("a:updated")[:10])
    print("TITLE:", title)
    print("AUTHORS:", "; ".join(authors))
    print("JREF:", jr.text if jr is not None else None, "| DOI:", doi.text if doi is not None else None, "| cats:", ",".join(cats[:4]))
    if full:
        print("ABSTRACT:", " ".join(g("a:summary").split()))
    print("-----")
mode = sys.argv[1]
if mode == "id":
    ids = ",".join(sys.argv[2:])
    data = q("http://export.arxiv.org/api/query?id_list=" + ids + "&max_results=100")
    root = ET.fromstring(data)
    for e in root.findall("a:entry", NS):
        show(e)
elif mode in ("search", "searchfull"):
    query = sys.argv[2]
    n = sys.argv[3] if len(sys.argv) > 3 else "30"
    data = q("http://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(query) + "&sortBy=submittedDate&sortOrder=descending&max_results=" + n)
    root = ET.fromstring(data)
    for e in root.findall("a:entry", NS):
        show(e, full=(mode == "searchfull"))
