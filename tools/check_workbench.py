"""Check a workbench before it is pushed: structure, tables, manifests, and that it holds nothing it shouldn't.

Standard library only, so that it keeps working. Format 1 of FORMAT.md in the mathematics-workbenches repository.
  python -I -B tools/check_workbench.py [ROOT]          check
  python -I -B tools/check_workbench.py [ROOT] --write  write the manifests first, for a version not yet deposited
"""
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(next((a for a in sys.argv[1:] if not a.startswith("--")), pathlib.Path(__file__).parent.parent)).resolve()
WRITE = "--write" in sys.argv
TEXT = {".md", ".tex", ".bib", ".tsv", ".csv", ".json", ".txt", ".py", ".sage", ".gp", ".lean", ".sha256", ".sty", ".cls"}
PLAIN = {"LICENSE", ".gitattributes", ".gitignore"}
HEADS = {
    "STATEMENTS.tsv": "tag\tversion\tnumber\tkind\tstatus\tstatement\tproof\tdepends_on\tsupersedes",
    "CHECK_EVENTS.tsv": "tag\tdate\twho\teffort\ttype\toutcome\trecord",
    "SOURCES.tsv": "key\tcitation\taddress\tused\thow_read",
}
STATUS = {"proved", "unchecked", "refuted", "withdrawn", "superseded", "open"}
TYPES = {"targeted proof check", "independent re-proof", "computation or formal certificate",
         "used and rechecked in this run", "carried as background without fault found",
         "discussed in an expert conference", "refuted, with the refined statement's id"}
TAG = re.compile("^WB-[0-9]{4}[.][0-9]{3}$")
BAD = {
    "a key or token": re.compile(b"sk-ant-[A-Za-z0-9]|sk-proj-[A-Za-z0-9]|ghp_[A-Za-z0-9]{20}|github_pat_[A-Za-z0-9]"),
    "an e-mail address": re.compile(b"[A-Za-z0-9._%+-]+@(?:gmail|outlook|hotmail|proton|protonmail|icloud|student)[.]"),
    "a local path": re.compile(b"[A-Za-z]:[/" + bytes([92, 92]) + b"]Users[/" + bytes([92, 92]) + b"]"),
}

wrong = []
files = [f for f in sorted(ROOT.rglob("*")) if f.is_file() and ".git" not in f.relative_to(ROOT).parts]
for need in ("README.md", "LICENSE", "workbench.json"):
    if not (ROOT / need).is_file():
        wrong.append("missing " + need)
for f in files:
    rel = f.relative_to(ROOT).as_posix()
    if f.suffix.lower() == ".pdf":
        if not f.with_suffix(".tex").is_file():
            wrong.append("a PDF without our TeX beside it: " + rel)
        continue
    if f.name not in PLAIN and f.suffix.lower() not in TEXT:
        wrong.append("a kind of file that doesn't belong: " + rel)
    data = f.read_bytes()
    if len(data) > 5_000_000:
        wrong.append("over 5 MB: " + rel)
    for what, rx in BAD.items():
        if f.name != "check_workbench.py" and rx.search(data):
            wrong.append("%s in %s" % (what, rel))
    if f.name in HEADS:
        lines = data.decode("utf-8").splitlines()
        if not lines or lines[0] != HEADS[f.name]:
            wrong.append("wrong header: " + rel)
            continue
        for i, line in enumerate(lines[1:], 2):
            row = line.split("\t")
            if len(row) != HEADS[f.name].count("\t") + 1:
                wrong.append("wrong number of fields: %s:%d" % (rel, i))
            elif f.name != "SOURCES.tsv" and not TAG.match(row[0]):
                wrong.append("not a permanent tag: %s:%d" % (rel, i))
            elif f.name == "STATEMENTS.tsv" and row[4] not in STATUS:
                wrong.append("unknown status: %s:%d" % (rel, i))
            elif f.name == "CHECK_EVENTS.tsv" and row[4] not in TYPES:
                wrong.append("unknown type of check: %s:%d" % (rel, i))

work = ROOT / "work"
for paper in (sorted(p for p in work.iterdir() if p.is_dir()) if work.is_dir() else []):
    if not re.match("^WB-[0-9]{4}$", paper.name):
        wrong.append("a work folder not named by its number: " + paper.name)
    for version in sorted(v for v in paper.iterdir() if v.is_dir()):
        for need in ("STATEMENTS.tsv", "CHECK_EVENTS.tsv", "SOURCES.tsv"):
            if not (version / need).is_file():
                wrong.append("missing %s in %s/%s" % (need, paper.name, version.name))
        own = [f for f in sorted(version.rglob("*")) if f.is_file() and f.name not in ("MANIFEST.sha256", "DEPOSITED.md")]
        text = "".join("%s  %s\n" % (hashlib.sha256(f.read_bytes()).hexdigest(), f.relative_to(version).as_posix()) for f in own)
        man = version / "MANIFEST.sha256"
        if WRITE and not (version / "DEPOSITED.md").is_file():
            man.write_text(text, encoding="utf-8", newline="\n")
        if not man.is_file() or man.read_text(encoding="utf-8") != text:
            wrong.append("manifest doesn't match: %s/%s" % (paper.name, version.name))

if (ROOT / "workbench.json").is_file():
    info = json.loads((ROOT / "workbench.json").read_text(encoding="utf-8"))
    if info.get("format") != 1:
        wrong.append("workbench.json doesn't state format 1")

for w in wrong:
    print("FAIL", w)
print("%s: %d files, %s" % (ROOT.name, len(files), "PASS" if not wrong else "%d faults" % len(wrong)))
sys.exit(1 if wrong else 0)
