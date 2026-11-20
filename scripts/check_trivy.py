"""Gate on fixable HIGH/CRITICAL vulnerabilities; report every severity."""
import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
blocking = [v for result in report.get("Results", []) for v in result.get("Vulnerabilities", []) if v.get("Severity") in {"HIGH", "CRITICAL"} and v.get("FixedVersion")]
for item in blocking:
    print(item["VulnerabilityID"], item["PkgName"], item["InstalledVersion"], "->", item["FixedVersion"])
print(f"Fixable HIGH/CRITICAL vulnerabilities: {len(blocking)}; all findings remain in the JSON report.")
raise SystemExit(bool(blocking))
