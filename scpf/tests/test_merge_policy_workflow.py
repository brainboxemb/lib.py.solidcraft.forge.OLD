from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "merge-policy.yml"
RELEASE = "v0.33.2"


class MergePolicyWorkflowTests(unittest.TestCase):
    def test_forge_wrapper_is_thin_and_uses_released_shared_policy(self):
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("# template: tool.cad.ci/merge-policy", text)
        self.assertIn("# template-version: 4", text)
        self.assertIn(f"# tool-release: {RELEASE}", text)
        self.assertIn("issue_comment:", text)
        self.assertIn("github.event.comment.body == '/merge'", text)
        self.assertIn(
            "startsWith(github.event.comment.body, '/merge-resolved')",
            text,
        )
        self.assertIn(
            "uses: brainboxemb/tool.cad.ci/.github/workflows/"
            f"reusable-merge-policy.yml@{RELEASE}",
            text,
        )

        self.assertIn("stable_branch: main", text)
        self.assertIn('development_branches: \'["dev-cad","dev-ci"]\'', text)
        self.assertIn(
            'permanent_branches: \'["build","gh-pages"]\'',
            text,
        )
        self.assertIn("integration_workflow: scpf.yml", text)

        for retired in (
            "stable_ref:",
            "lane_refs_json:",
            "permanent_refs_json:",
            "temporary_prefixes_json:",
            "temporary_branch_prefixes:",
            "github.actor == github.repository_owner",
        ):
            self.assertNotIn(retired, text)

        for value in (
            "pull-requests: write",
            "issues: write",
            "checks: read",
            "statuses: read",
            "actions: write",
            "contents: write",
        ):
            self.assertIn(value, text)

    def test_forge_wrapper_contains_no_local_merge_or_bulk_cleanup_logic(self):
        text = WORKFLOW.read_text(encoding="utf-8")

        for forbidden in (
            "runs-on:",
            "gh api",
            "scripts/merge_policy.py",
            "merge_method",
            "check-runs?per_page=100",
            "/cleanup-branches",
            "pulls?state=closed",
            "compare/$encoded",
            "git/refs/heads/$source_branch",
        ):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
