#!/usr/bin/env python3
"""Test the current example-driven Forge documentation source."""

from __future__ import annotations

import html
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
sys.path.insert(0, str(ROOT / "scpf"))

from html_writer import (
    qualification_current_evidence,
    qualification_reference_comparison,
    qualification_setup_svg,
)
from qualification_view import _expected_body_rows, _raw_file_rows


class SiteSourceTests(unittest.TestCase):
    def test_site_orchestrator_keeps_html_in_explicit_render_layer(self):
        build = (SITE / "build.py").read_text(encoding="utf-8")
        guides = (SITE / "guides.py").read_text(encoding="utf-8")

        for token in (
            "from qualification.",
            "import qualification.",
            "EXAMPLES =",
            "SCHEMATICS =",
            "COPY_SCRIPT =",
            "SEARCH_SCRIPT =",
            "CHEATSHEET =",
            "SECTION_PRESENTATION =",
        ):
            self.assertNotIn(token, build)

        for markup in (
            "<!doctype html",
            "<main",
            "<section",
            "<article",
            "<table",
            "<li",
            "<a ",
        ):
            self.assertNotIn(markup, build.lower())
        self.assertIn("from html_writer import", build)
        self.assertNotIn("GUIDES = [", guides)
        self.assertNotIn("<h2", guides)

        self.assertTrue((SITE / "html_writer.py").is_file())
        self.assertTrue((SITE / "build_evidence.py").is_file())
        self.assertTrue((SITE / "qualification_view.py").is_file())
        self.assertTrue((SITE / "templates" / "page.html").is_file())
        self.assertTrue((SITE / "templates" / "guide-overview.html").is_file())
        self.assertTrue((SITE / "templates" / "example.html").is_file())
        self.assertTrue((SITE / "templates" / "home.html").is_file())
        self.assertTrue((SITE / "templates" / "api-design-contract.html").is_file())
        self.assertTrue((SITE / "templates" / "reference-overview.html").is_file())
        self.assertTrue((SITE / "templates" / "cheatsheet-item.html").is_file())
        self.assertTrue((SITE / "templates" / "cheatsheet-section.html").is_file())
        self.assertTrue((SITE / "templates" / "qualification-current.html").is_file())
        self.assertTrue((SITE / "templates" / "qualification-reference-row.html").is_file())
        self.assertTrue((SITE / "templates" / "qualification-visual-section.html").is_file())
        self.assertTrue((SITE / "templates" / "qualification-diagrams.html").is_file())
        self.assertTrue((SITE / "static" / "copy.js").is_file())
        self.assertTrue((SITE / "static" / "search.js").is_file())
        self.assertTrue((SITE / "content" / "guides.json").is_file())
        self.assertTrue((SITE / "content" / "cheatsheet.yml").is_file())
        self.assertTrue(
            (SITE / "content" / "verification-sections.yml").is_file()
        )
        self.assertTrue(
            (SITE / "templates" / "verification-group.html").is_file()
        )
        self.assertTrue(
            (SITE / "templates" / "verification-coverage.html").is_file()
        )
        self.assertTrue(
            (SITE / "templates" / "verification-results.html").is_file()
        )
        self.assertTrue(
            (SITE / "templates" / "verification-joint-anatomy.html").is_file()
        )
        self.assertTrue(
            (SITE / "templates" / "legacy-redirect.html").is_file()
        )
        self.assertTrue((SITE / "verification_special.py").is_file())

    def test_verification_pages_keep_inline_source_comparison(self):
        build = (SITE / "build.py").read_text(encoding="utf-8")
        case_template = (
            SITE / "templates" / "qualification-case.html"
        ).read_text(encoding="utf-8")
        reference_template = (
            SITE / "templates" / "qualification-reference-row.html"
        ).read_text(encoding="utf-8")

        self.assertIn("${forge_source}", case_template)
        self.assertIn("${source_code}", reference_template)
        self.assertIn("qualification_reference_comparison(", build)
        self.assertIn(
            "from build_evidence import IMPLEMENTATIONS",
            build,
        )
        self.assertIn("for implementation in IMPLEMENTATIONS", build)

    def test_verification_case_keeps_historical_information_order(self):
        case_template = (
            SITE / "templates" / "qualification-case.html"
        ).read_text(encoding="utf-8")
        headings = (
            "What this example makes",
            "Forge code",
            "${reference_comparison}",
            "How Forge builds it in SolidCraft",
            "${current_evidence}",
            "Sources of truth",
        )
        positions = [case_template.index(value) for value in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("${setup_diagram}", case_template)
        self.assertIn("${case_preview}", case_template)
        self.assertNotIn("Engineering explanation", case_template)

        index_template = (
            SITE / "templates" / "qualification-index.html"
        ).read_text(encoding="utf-8")
        self.assertNotIn("${diagrams}", index_template)

    def test_technical_details_keep_test_order_and_structured_raw_files(self):
        template = (
            SITE / "templates" / "qualification-current.html"
        ).read_text(encoding="utf-8")
        headings = (
            "Verification checks",
            "Geometry evidence",
            "Saved-design test",
            "Raw test files",
            "Reference documentation",
        )
        positions = [template.index(value) for value in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("${raw_files}", template)
        self.assertNotIn("${raw_links}", template)
        self.assertNotIn('class="evidence-links"', template)

        writer = (SITE / "html_writer.py").read_text(encoding="utf-8")
        self.assertNotIn('raw_links = " · ".join', writer)
        self.assertIn("qualification_raw_files(", writer)

    def test_raw_file_inventory_enumerates_complete_durable_item(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            item_root = root / "examples" / "sheet-fold"
            wanted = (
                "solidcraft.json",
                "model_verify/verification.json",
                "model_verify/native/model.sc",
                "model_verify/visual/front/actual.png",
                "pythonscad/references/sheet-fold/pythonscad/model.stl",
                "build123d/references/sheet-fold/build123d/verification.json",
            )
            for relative in wanted:
                path = item_root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"x")
            internal = item_root / ".cad-ci" / "item.json"
            internal.parent.mkdir(parents=True, exist_ok=True)
            internal.write_bytes(b"x")

            stable = SimpleNamespace(
                root=root,
                blob_url=lambda path: (
                    "https://build.invalid/"
                    + path.relative_to(root).as_posix()
                ),
            )
            example = SimpleNamespace(slug="sheet-fold")
            rows = _raw_file_rows(stable, example)
            paths = {row["path"] for row in rows}

            self.assertEqual(paths, set(wanted))
            self.assertNotIn(".cad-ci/item.json", paths)
            self.assertGreater(len(rows), 5)
            groups = {row["group"] for row in rows}
            self.assertIn("solidcraft", groups)
            self.assertIn("visual", groups)
            self.assertIn("pythonscad", groups)
            self.assertIn("build123d", groups)

    def test_raw_test_files_render_as_descriptive_lists(self):
        view = {
            "status": "pass",
            "checks": {},
            "parameters": (),
            "bodies": (),
            "verification_checks": (),
            "saved_designs": (),
            "visual_views": (),
            "site_source_commit": "site-source",
            "accepted_source_commit": "accepted-source",
            "build_commit": "build-source",
            "source_files": (
                {
                    "label": "Forge model source",
                    "path": "examples/demo/scpf/model.py",
                    "url": "https://source.invalid/model.py",
                },
                {
                    "label": "Integration contract test",
                    "path": "examples/demo/tests/test_contract.py",
                    "url": "https://source.invalid/test_contract.py",
                },
            ),
            "raw_files": tuple(
                {
                    "group": "solidcraft",
                    "group_label": "SolidCraft model and verification evidence",
                    "label": f"Evidence {index}",
                    "path": f"model_verify/file-{index}.json",
                    "url": f"https://build.invalid/file-{index}.json",
                }
                for index in range(12)
            ),
        }
        rendered = qualification_current_evidence(
            view,
            "Demo",
            saved_design_test="Not required.",
            bounds_sufficient="yes",
            geometry_reason="Bounds fully describe this demo.",
            reference_notes="",
        )
        self.assertIn("<ul", rendered)
        self.assertIn("Accepted source files", rendered)
        self.assertIn("SolidCraft model and verification evidence", rendered)
        self.assertIn("(12 files)", rendered)
        self.assertIn("test_contract.py", rendered)
        self.assertNotIn('class="evidence-links"', rendered)
        self.assertNotIn(">commands</a> ·", rendered)

    def test_setup_diagram_uses_declared_target_envelopes(self):
        svg = qualification_setup_svg(
            {
                "expected_bodies": (
                    {
                        "label": "Plate",
                        "minimum": [-50.0, -50.0, 0.0],
                        "maximum": [50.0, 50.0, 6.0],
                    },
                ),
            },
            "Example plate",
        )
        self.assertIn("Expected setup", svg)
        self.assertIn("Plate", svg)
        self.assertIn('viewBox="0 0 640 360"', svg)

    def test_setup_target_envelopes_include_body_groups(self):
        rows = _expected_body_rows(
            {
                "checks": [
                    {
                        "evidence": {
                            "body_groups": [
                                {
                                    "body_envelopes": {
                                        "matched_pairs": [
                                            {
                                                "actual": {"label": "Block"},
                                                "expected": {
                                                    "min": [-20.0, -15.0, 0.0],
                                                    "max": [20.0, 15.0, 10.0],
                                                },
                                            },
                                            {
                                                "actual": {
                                                    "label": "Block (Block:2)"
                                                },
                                                "expected": {
                                                    "min": [20.0, -15.0, 0.0],
                                                    "max": [60.0, 15.0, 10.0],
                                                },
                                            },
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["label"], "Block")
        self.assertEqual(rows[1]["label"], "Block (Block:2)")

    def test_public_templates_use_verification_terminology(self):
        for path in (SITE / "templates").glob("*.html"):
            source = path.read_text(encoding="utf-8")
            with self.subTest(template=path.name):
                self.assertNotIn("Qualification", source)
                self.assertNotIn("/qualification/", source)

    def test_reference_source_is_rendered_beside_each_current_result(self):
        implementations = ("pythonscad", "pybosl2", "cadquery", "build123d")
        sources = {
            name: f"# unique source for {name}\nMODEL = '{name}'\n"
            for name in implementations
        }
        view = {
            "status": "pass",
            "checks": {},
            "parameters": (),
            "bodies": (),
            "verification_checks": (),
            "saved_designs": (),
            "visual_views": (),
            "site_source_commit": "site-source",
            "accepted_source_commit": "model-source",
            "build_commit": "build-commit",
            "preview_url": "preview.png",
            "commands_url": "commands.json",
            "verification_url": "verification.json",
            "measurements_url": "measurements.json",
            "native_model_url": "model.sc",
            "native_step_url": "model.step",
            "native_results_url": "results.json",
            "preview_metadata_url": "preview.json",
            "references": tuple(
                {
                    "implementation": name,
                    "status": "pass",
                    "accepted_source_commit": f"source-{name}",
                    "source_url": f"https://accepted.invalid/{name}.py",
                    "stl_url": f"https://example.invalid/{name}.stl",
                    "verification_url": f"https://example.invalid/{name}.json",
                    "preview_metadata_url": f"https://example.invalid/{name}-preview.json",
                    "preview_url": f"https://example.invalid/{name}.png",
                    "geometry_json": '{"status": "pass"}',
                }
                for name in implementations
            ),
        }

        source_urls = {
            name: f"https://current.invalid/{name}.py"
            for name in implementations
        }
        rendered = qualification_reference_comparison(
            sources,
            source_urls,
            reference_rows=view["references"],
        )

        for name in implementations:
            with self.subTest(implementation=name):
                self.assertIn(f"unique source for {name}", rendered)
                self.assertIn(f"{name}.png", rendered)
                self.assertIn(f"{name}.stl", rendered)
                self.assertIn(
                    f"https://current.invalid/{name}.py",
                    rendered,
                )
                self.assertIn(
                    f"https://accepted.invalid/{name}.py",
                    rendered,
                )

    def test_site_cli_and_workflow_use_long_lived_complete_scopes(self):
        build = (SITE / "build.py").read_text(encoding="utf-8")

        for required in (
            "--build-evidence",
            "--build-scope",
            "--build-commit",
        ):
            self.assertIn(required, build)
        for retired in (
            "--build-main",
            "--native",
            "--diagram-root",
            "--references",
            "--evidence-sha",
            "--build-manifest",
        ):
            self.assertNotIn(retired, build)

        workflow = (
            ROOT / ".github" / "workflows" / "scpf.yml"
        ).read_text(encoding="utf-8")
        tool_revision = (
            "b1474f6be66dc0236f2a5c2555af07a100447255"
        )
        self.assertIn(
            f"brainboxemb/tool.cad.ci@{tool_revision}",
            workflow,
        )
        self.assertEqual(workflow.count('jobs: "2"'), 2)
        self.assertNotIn("reusable-pr.yml", workflow)
        self.assertNotIn("build prepare-pr", workflow)
        self.assertNotIn("build-cleanup", workflow)
        self.assertNotIn("pages-cleanup", workflow)
        self.assertNotIn("actions/upload-artifact", workflow)
        self.assertNotIn("actions/download-artifact", workflow)

        self.assertIn("branches: [main, dev-cad, dev-ci]", workflow)
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("types: [opened, synchronize, reopened]", workflow)

        pr = workflow.split("  cad_ci_pr:", 1)[1].split(
            "  cad_ci_push:", 1
        )[0]
        self.assertEqual(pr.count("runs-on: ubuntu-latest"), 1)
        self.assertIn("contents: read", pr)
        self.assertNotIn("contents: write", pr)
        self.assertIn(
            "source_sha: ${{ github.event.pull_request.head.sha }}",
            pr,
        )
        self.assertIn(
            "base_sha: ${{ github.event.pull_request.base.sha }}",
            pr,
        )
        self.assertNotIn("publish build", pr)
        self.assertNotIn("publish pages", pr)

        push = workflow.split("  cad_ci_push:", 1)[1]
        self.assertIn(
            "github.event_name == 'push' || github.event_name == 'workflow_dispatch'",
            push,
        )
        self.assertEqual(push.count("runs-on: ubuntu-latest"), 1)
        self.assertIn(
            "group: forge-push-${{ github.repository }}-${{ github.ref_name }}",
            push,
        )
        self.assertIn("cancel-in-progress: true", push)
        self.assertIn("main|dev-cad|dev-ci", push)
        self.assertIn(
            "durable_scope: ${{ github.ref_name }}",
            push,
        )
        self.assertIn(
            "source_ref: ${{ github.ref_name }}",
            push,
        )
        self.assertIn(
            "BUILD_COMMIT: ${{ steps.cad_ci.outputs.build_commit }}",
            push,
        )
        self.assertIn(
            "PREPARED_SCOPE: ${{ steps.cad_ci.outputs.prepared_scope }}",
            push,
        )
        self.assertIn('--build-evidence "$PREPARED_SCOPE"', push)
        self.assertIn('--build-scope "$SCOPE"', push)
        self.assertIn("--preserve-subtree dev-cad", push)
        self.assertIn("--preserve-subtree dev-ci", push)
        self.assertIn('page_args=(--name "$SCOPE")', push)
        self.assertIn(
            "generated-site/verification/manifest.json",
            push,
        )
        self.assertNotIn(
            "generated-site/qualification/manifest.json",
            push,
        )

        for retired in (
            "Resolve durable source scope",
            "Fetch current durable build branch",
            "Prepare complete durable scope",
            "Publish complete durable scope",
            "python -m cad_ci_tool build fetch",
            "python -m cad_ci_tool build update-main",
            "python -m cad_ci_tool build update-named",
            "python -m cad_ci_tool build prepare-named",
            "python -m cad_ci_tool publish build",
            "FETCH_HEAD:",
            "scope_exists=false",
        ):
            self.assertNotIn(retired, push)

        self.assertNotIn("actions/setup-python", push)
        self.assertNotIn("pip install", push)


    def test_source_only_site_build_discovers_all_examples(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "site"
            subprocess.run(
                [
                    sys.executable,
                    str(SITE / "build.py"),
                    "--out",
                    str(out),
                    "--source-sha",
                    "source-test",
                ],
                cwd=ROOT,
                check=True,
            )

            manifest = json.loads(
                (out / "manifest.json").read_text(encoding="utf-8")
            )
            expected_count = len(
                tuple((ROOT / "examples").glob("*/model.yml"))
            )
            self.assertEqual(len(manifest["examples"]), expected_count)

            verification = json.loads(
                (out / "verification" / "manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                len(verification["cases"]),
                expected_count,
            )
            self.assertEqual(
                verification["evidence_source"],
                "build/main",
            )

            simple_case = verification["cases"]["simple-box"]
            self.assertEqual(
                simple_case["documentation_source"],
                "examples/simple-box/README.md",
            )

            for slug in manifest["examples"]:
                with self.subTest(slug=slug):
                    self.assertTrue(
                        (out / "examples" / slug / "index.html").is_file()
                    )
                    self.assertTrue(
                        (
                            out
                            / "verification"
                            / slug
                            / "index.html"
                        ).is_file()
                    )

            simple_page = (
                out / "examples" / "simple-box" / "index.html"
            ).read_text(encoding="utf-8")
            self.assertIn(
                "Establish the smallest model/parameter contract",
                simple_page,
            )
            self.assertIn(
                "parameters.add for the public dimensions",
                simple_page,
            )
            self.assertIn(
                "cube([40,30,10]) is the constructive-geometry baseline",
                simple_page,
            )
            self.assertIn(
                "Its body size fully describes the visible geometry",
                simple_page,
            )

            for special in ("results", "coverage", "joint-anatomy"):
                self.assertTrue(
                    (
                        out
                        / "verification"
                        / special
                        / "index.html"
                    ).is_file()
                )
                self.assertTrue(
                    (
                        out
                        / "qualification"
                        / special
                        / "index.html"
                    ).is_file()
                )

            results_page = (
                out / "verification" / "results" / "index.html"
            ).read_text(encoding="utf-8")
            self.assertIn("Verification results", results_page)
            self.assertIn("Current case results", results_page)
            for slug in manifest["examples"]:
                self.assertIn(
                    f'href="../{slug}/"',
                    results_page,
                )

            coverage_page = (
                out / "verification" / "coverage" / "index.html"
            ).read_text(encoding="utf-8")
            for heading in (
                "SolidCraft functionality coverage",
                "SolidCraft → Forge support",
                "Coverage by area",
                "Capability detail",
                "Functional verification",
                "Verification by area",
                "Verification detail",
                "Public Python API exports",
            ):
                self.assertIn(heading, coverage_page)
            self.assertIn("as-built-attach", coverage_page)
            self.assertIn("parametric-placement-pair", coverage_page)
            self.assertNotIn(">Qualification<", coverage_page)

            joint_page = (
                out / "verification" / "joint-anatomy" / "index.html"
            ).read_text(encoding="utf-8")
            for heading in (
                "Placing a corner bracket with Forge",
                "Wat is een joint origin? / What is a joint origin?",
                "Where does the joint-origin frame come from?",
                "What the current Forge code is doing",
                "Requirements for the Forge API",
                "Verification order",
                "Native SolidCraft references",
            ):
                self.assertIn(heading, joint_page)
            for name in (
                "corner-bracket-goal",
                "corner-bracket-depth",
                "solidcraft-joint-anatomy",
                "solidcraft-joint-references",
                "corner-bracket-local-axes",
                "corner-bracket-front-corners",
            ):
                self.assertTrue(
                    (
                        out
                        / "verification"
                        / "joint-anatomy"
                        / f"{name}.cadcraft.json"
                    ).is_file()
                )
                self.assertTrue(
                    (
                        out
                        / "qualification"
                        / "joint-anatomy"
                        / f"{name}.cadcraft.json"
                    ).is_file()
                )

            legacy_root = (
                out / "qualification" / "index.html"
            ).read_text(encoding="utf-8")
            self.assertIn("../verification/", legacy_root)
            self.assertNotIn(">Qualification<", legacy_root)
            for slug in manifest["examples"]:
                redirect = (
                    out / "qualification" / slug / "index.html"
                ).read_text(encoding="utf-8")
                self.assertIn(
                    f"../../verification/{slug}/",
                    redirect,
                )

            self.assertEqual(
                (out / "qualification" / "manifest.json").read_text(
                    encoding="utf-8"
                ),
                (out / "verification" / "manifest.json").read_text(
                    encoding="utf-8"
                ),
            )

            verification_index = (
                out / "verification" / "index.html"
            ).read_text(encoding="utf-8")
            for heading in (
                "1 · Basic geometry",
                "2 · Parent/child features and faces",
                "3 · Parameters and dependencies",
                "4 · Components and occurrences",
                "5 · Anchors and local frames",
                "6 · Associative relationships",
            ):
                self.assertIn(heading, verification_index)
            self.assertLess(
                verification_index.index("Parameterized Box"),
                verification_index.index("TOP Sketch on circular body"),
            )
            self.assertLess(
                verification_index.index("Face anchor follows parent geometry"),
                verification_index.index("Topology-backed corner anchor"),
            )

            verification_case = (
                out / "verification" / "simple-box" / "index.html"
            ).read_text(encoding="utf-8")
            self.assertIn("Forge code", verification_case)
            self.assertIn("class SimpleBox", verification_case)
            self.assertIn("Verification", verification_case)
            self.assertIn("1 · Basic geometry", verification_case)
            self.assertNotIn(">fundamentals<", verification_case)
            self.assertNotIn(">Qualification<", verification_case)
            for implementation in (
                "pythonscad",
                "pybosl2",
                "cadquery",
                "build123d",
            ):
                reference_source = (
                    ROOT
                    / "examples"
                    / "simple-box"
                    / implementation
                    / "model.py"
                ).read_text(encoding="utf-8")
                self.assertIn(
                    html.escape(
                        reference_source.strip().splitlines()[0],
                        quote=True,
                    ),
                    verification_case,
                )
            self.assertIn(
                "Stable result evidence is not available",
                verification_case,
            )

            home = (out / "index.html").read_text(encoding="utf-8")
            self.assertIn("static/copy.js", home)
            self.assertIn("static/search.js", home)
            self.assertNotIn("<script>(() =>", home)

            search = json.loads(
                (out / "search-index.json").read_text(encoding="utf-8")
            )
            example_entries = [
                row for row in search["entries"]
                if row["kind"] == "Example"
            ]
            self.assertEqual(
                len(example_entries),
                expected_count,
            )


if __name__ == "__main__":
    unittest.main()
