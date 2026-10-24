"""Read one chat-completion response (JSON on stdin) and print a one-line verdict on the seller reply format.
FORMAT-OK = the reply parses as JSON and carries an "ask" key; WRONG-SCHEMA = JSON without an ask; NOT-JSON otherwise."""
import json
import sys

raw = sys.stdin.read()
try:
    d = json.loads(raw)
    content = (d["choices"][0]["message"].get("content") or "").strip()
    i, j = content.find("{"), content.rfind("}")
    keys = sorted(json.loads(content[i:j + 1]).keys())
    tokens = d.get("usage", {}).get("completion_tokens")
    print(("FORMAT-OK" if "ask" in keys else "WRONG-SCHEMA") + f" tokens={tokens} keys={keys} prefix={content[:60]!r}")
except Exception as e:  # empty body during a cold start, HTML error page, malformed JSON
    print("NOT-JSON", str(e)[:60], "body:", raw[:120].replace("\n", " "))
