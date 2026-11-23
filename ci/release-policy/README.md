# Release policy

This CI item tests the Forge-owned part of release publication.

Forge owns only:

- package-version agreement;
- dated CHANGELOG release notes;
- `TESTED_SOLIDCRAFT_VERSION`;
- `docs/background/design/release-blockers.txt`;
- the thin consumer wrapper pointing at the exact released CAD release flow.

Released `tool.cad.ci` owns the stable main `ci-build-record` check.
Released `tool.py.lib.ci` owns `/release` parsing, stable-main checking,
annotated tag/GitHub Release creation, idempotency and issue reporting.

Pages is web output and is not release evidence.
