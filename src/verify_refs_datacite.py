"""Verify every arXiv id in refs.json against DataCite (arXiv's DOI registrar: 10.48550/arXiv.<id>) while export.arxiv.org is down.
Title match = normalized title equality or one contained in the other (>= 0.85 of the shorter); author match = surname appears in creators."""
import json, re, sys, time, urllib.request
refs = json.load(open(sys.argv[1], encoding="utf-8"))
def norm(s): return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
rows, ok = [], 0
for r in refs:
    rid = r["id"]
    if not re.match(r"^\d{4}\.\d{4,5}(v\d+)?$", rid):
        rows.append((rid, "SKIP (not an arXiv id)", r.get("title", "")[:60])); continue
    url = f"https://api.datacite.org/dois/10.48550/arXiv.{rid.split('v')[0]}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "caiac-ref-check"}), timeout=20) as f:
            a = json.load(f)["data"]["attributes"]
    except Exception as e:
        rows.append((rid, f"ERROR {type(e).__name__}", r.get("title", "")[:60])); continue
    t_dc = norm(a["titles"][0]["title"]); t_ref = norm(r.get("title", ""))
    tmatch = t_dc == t_ref or t_ref in t_dc or t_dc in t_ref or (len(t_ref) > 20 and t_ref[:int(0.85 * len(t_ref))] in t_dc)
    creators = " ".join(c.get("name", "") + " " + c.get("familyName", "") for c in a.get("creators", [])).lower()
    au = (r.get("author") or "").lower().split()[-1] if r.get("author") else ""
    amatch = (au in creators) if au else True
    status = "OK" if (tmatch and amatch) else ("TITLE MISMATCH" if not tmatch else "AUTHOR MISMATCH")
    ok += status == "OK"
    rows.append((rid, status, a["titles"][0]["title"][:70] + (" | " + a["creators"][0].get("name", "") if a.get("creators") else "")))
    time.sleep(0.15)
print(f"{ok} OK of {sum(1 for x in rows if not x[1].startswith('SKIP'))} arXiv ids checked; {sum(1 for x in rows if x[1].startswith('SKIP'))} skipped")
for x in rows:
    if x[1] != "OK": print(" ", *x)
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write("# Reference check via DataCite (export.arxiv.org unreachable from this network at 10:40 PM ET, Oct 25)\n\n")
    f.write(f"{ok} OK of {sum(1 for x in rows if not x[1].startswith('SKIP'))} arXiv ids; each row: id, status, DataCite title | first creator.\n\n")
    for x in rows: f.write(f"- {x[0]} · {x[1]} · {x[2]}\n")
