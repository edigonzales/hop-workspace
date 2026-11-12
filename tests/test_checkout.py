"""Exercise the real checkout script using disposable, offline Git remotes."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "checkout.sh"
REPOSITORIES = ("hop-alpha", "hop-beta")


class CheckoutTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="hop workspace test ")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.workspace = self.base / "workspace with spaces"
        self.workspace.mkdir()
        self.script = self.workspace / "checkout.sh"
        shutil.copy2(SCRIPT, self.script)
        self.inventory = self.workspace / "repositories.txt"
        self.inventory.write_text("\n".join(REPOSITORIES) + "\n")
        (self.workspace / ".gitignore").write_text(
            "".join(f"/{name}/\n" for name in REPOSITORIES)
        )

        # Neither user Git settings/identity nor inherited repository selectors
        # should affect the fixtures. URL rewrites are process-local, not global.
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith("GIT_")}
        self.env.update({
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": str(self.base / "empty-gitconfig"),
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_AUTHOR_NAME": "Workspace Test",
            "GIT_AUTHOR_EMAIL": "workspace@example.invalid",
            "GIT_COMMITTER_NAME": "Workspace Test",
            "GIT_COMMITTER_EMAIL": "workspace@example.invalid",
        })
        self.remotes = self.base / "remotes"
        self.remotes.mkdir()
        self.seeds = {}
        rewrites = []
        for name in REPOSITORIES:
            remote = self.remotes / f"{name}.git"
            for url in self.origin_urls(name):
                rewrites.append((f"url.{remote.as_uri()}.insteadOf", url))
        self.env["GIT_CONFIG_COUNT"] = str(len(rewrites))
        for index, (key, value) in enumerate(rewrites):
            self.env[f"GIT_CONFIG_KEY_{index}"] = key
            self.env[f"GIT_CONFIG_VALUE_{index}"] = value

        self.git(self.base, "init", "--initial-branch=main", str(self.workspace))
        for name in REPOSITORIES:
            remote = self.remotes / f"{name}.git"
            seed = self.base / f"seed {name}"
            self.git(self.base, "init", "--bare", "--initial-branch=main", str(remote))
            self.git(self.base, "init", "--initial-branch=main", str(seed))
            (seed / "data.txt").write_text("initial\n")
            self.git(seed, "add", "data.txt")
            self.git(seed, "commit", "-m", "Initial fixture")
            self.git(seed, "remote", "add", "origin", remote.as_uri())
            self.git(seed, "push", "origin", "main")
            self.seeds[name] = seed

    @staticmethod
    def origin_urls(name):
        return tuple(prefix + name + suffix
                     for prefix in ("https://github.com/edigonzales/",
                                    "git@github.com:edigonzales/",
                                    "ssh://git@github.com/edigonzales/")
                     for suffix in ("", ".git"))

    def git(self, directory, *args):
        result = subprocess.run(
            ["git", "-C", str(directory), *args], env=self.env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout.strip()

    def run_script(self, *args, code=0):
        # Always run outside the workspace; both paths contain spaces.
        result = subprocess.run(
            [str(self.script), *args], cwd=self.base, env=self.env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def advance(self, name):
        seed = self.seeds[name]
        (seed / "data.txt").write_text("remote update\n")
        self.git(seed, "commit", "-am", "Remote update")
        self.git(seed, "push", "origin", "main")
        return self.git(seed, "rev-parse", "HEAD")

    def assert_blocked(self, diagnostic, fetch_allowed=False):
        repo = self.workspace / "hop-alpha"
        head = self.git(repo, "rev-parse", "HEAD")
        branch = self.git(repo, "rev-parse", "--abbrev-ref", "HEAD")
        status = self.git(repo, "status", "--porcelain")
        fetch_head = repo / ".git" / "FETCH_HEAD"
        old_fetch = fetch_head.read_bytes() if fetch_head.exists() else None
        output = self.run_script("hop-alpha", code=1)
        self.assertIn(diagnostic, output)
        self.assertEqual(self.git(repo, "rev-parse", "HEAD"), head)
        self.assertEqual(self.git(repo, "rev-parse", "--abbrev-ref", "HEAD"), branch)
        self.assertEqual(self.git(repo, "status", "--porcelain"), status)
        self.assertEqual(self.git(repo, "stash", "list"), "")
        if not fetch_allowed:
            self.assertEqual(fetch_head.read_bytes() if fetch_head.exists() else None,
                             old_fetch)

    def test_clone_all_on_main_and_ignore_independent_repositories(self):
        sibling = self.base / "hop-alpha"
        sibling.mkdir()
        (sibling / "keep.txt").write_text("existing neighboring checkout\n")
        self.run_script()
        for name in REPOSITORIES:
            repo = self.workspace / name
            self.assertEqual(self.git(repo, "branch", "--show-current"), "main")
            self.assertEqual(self.git(repo, "rev-parse", "--show-toplevel"), str(repo))
            self.assertEqual(self.git(repo, "config", "--get", "remote.origin.url"),
                             f"https://github.com/edigonzales/{name}.git")
            self.assertEqual(self.git(repo, "rev-parse", "HEAD"),
                             self.git(self.seeds[name], "rev-parse", "HEAD"))
            self.assertEqual(self.git(repo, "status", "--porcelain"), "")
            self.assertEqual(self.git(self.workspace, "check-ignore", name), name)
        self.assertEqual((sibling / "keep.txt").read_text(),
                         "existing neighboring checkout\n")
        self.assertEqual(self.git(self.workspace, "ls-files", "--stage"), "")

    def test_select_only_requested_repository(self):
        self.run_script("hop-beta")
        self.assertTrue((self.workspace / "hop-beta" / ".git").is_dir())
        self.assertFalse((self.workspace / "hop-alpha").exists())

    def test_repeated_run_is_idempotent(self):
        self.run_script()
        heads = {name: self.git(self.workspace / name, "rev-parse", "HEAD")
                 for name in REPOSITORIES}
        self.run_script()
        for name, head in heads.items():
            self.assertEqual(self.git(self.workspace / name, "rev-parse", "HEAD"), head)

    def test_fast_forward(self):
        self.run_script("hop-alpha")
        head = self.advance("hop-alpha")
        self.run_script("hop-alpha")
        repo = self.workspace / "hop-alpha"
        self.assertEqual(self.git(repo, "rev-parse", "HEAD"), head)
        self.assertEqual((repo / "data.txt").read_text(), "remote update\n")
        self.assertEqual(self.git(repo, "status", "--porcelain"), "")

    def test_local_ahead_commits_are_preserved(self):
        self.run_script("hop-alpha")
        repo = self.workspace / "hop-alpha"
        (repo / "local.txt").write_text("local commit\n")
        self.git(repo, "add", "local.txt")
        self.git(repo, "commit", "-m", "Local work")
        head = self.git(repo, "rev-parse", "HEAD")
        self.run_script("hop-alpha")
        self.assertEqual(self.git(repo, "rev-parse", "HEAD"), head)
        self.assertEqual(self.git(repo, "rev-list", "--count", "origin/main..main"), "1")

    def test_unstaged_changes_are_preserved(self):
        self.run_script("hop-alpha")
        path = self.workspace / "hop-alpha" / "data.txt"
        path.write_text("local changes\n")
        self.advance("hop-alpha")
        self.assert_blocked("Lokale Änderungen")
        self.assertEqual(path.read_text(), "local changes\n")

    def test_staged_changes_are_preserved(self):
        self.run_script("hop-alpha")
        repo = self.workspace / "hop-alpha"
        (repo / "data.txt").write_text("staged changes\n")
        self.git(repo, "add", "data.txt")
        self.assert_blocked("Lokale Änderungen")
        self.assertEqual((repo / "data.txt").read_text(), "staged changes\n")

    def test_untracked_files_are_preserved(self):
        self.run_script("hop-alpha")
        path = self.workspace / "hop-alpha" / "untracked.txt"
        path.write_text("untracked work\n")
        self.assert_blocked("unversionierte Dateien")
        self.assertEqual(path.read_text(), "untracked work\n")

    def test_feature_branch_is_not_switched(self):
        self.run_script("hop-alpha")
        self.git(self.workspace / "hop-alpha", "checkout", "-b", "feature")
        self.assert_blocked("Branch ist feature")

    def test_detached_head_is_not_switched(self):
        self.run_script("hop-alpha")
        self.git(self.workspace / "hop-alpha", "checkout", "--detach")
        self.assert_blocked("detached HEAD")

    def test_divergence_does_not_merge_or_reset(self):
        self.run_script("hop-alpha")
        repo = self.workspace / "hop-alpha"
        (repo / "local.txt").write_text("local commit\n")
        self.git(repo, "add", "local.txt")
        self.git(repo, "commit", "-m", "Local work")
        self.advance("hop-alpha")
        self.assert_blocked("FEHLER", fetch_allowed=True)
        self.assertFalse((repo / ".git" / "MERGE_HEAD").exists())

    def test_wrong_origin_is_rejected_before_fetch(self):
        self.run_script("hop-alpha")
        self.git(self.workspace / "hop-alpha", "remote", "set-url", "origin",
                 "https://github.com/someone-else/hop-alpha.git")
        self.assert_blocked("Origin entspricht nicht")

    def test_missing_origin_is_rejected_before_fetch(self):
        self.run_script("hop-alpha")
        self.git(self.workspace / "hop-alpha", "remote", "remove", "origin")
        self.assert_blocked("Origin entspricht nicht")

    def test_https_and_ssh_origin_spellings(self):
        self.run_script("hop-alpha")
        for url in self.origin_urls("hop-alpha"):
            with self.subTest(url=url):
                self.git(self.workspace / "hop-alpha", "remote", "set-url", "origin", url)
                self.run_script("hop-alpha")

    def test_directory_inheriting_parent_git_is_rejected(self):
        destination = self.workspace / "hop-alpha"
        destination.mkdir()
        self.assertIn("kein eigenes Git-Toplevel", self.run_script("hop-alpha", code=1))
        self.assertEqual(list(destination.iterdir()), [])

    def test_file_collision_is_preserved(self):
        destination = self.workspace / "hop-alpha"
        destination.write_text("keep this file\n")
        self.assertIn("Zielpfad ist belegt", self.run_script("hop-alpha", code=1))
        self.assertEqual(destination.read_text(), "keep this file\n")

    def test_symlinks_are_rejected(self):
        destination = self.workspace / "hop-alpha"
        for target in (self.seeds["hop-alpha"], self.base / "missing"):
            with self.subTest(target=target):
                destination.symlink_to(target, target_is_directory=True)
                try:
                    self.assertIn("Symlink", self.run_script("hop-alpha", code=1))
                    self.assertTrue(destination.is_symlink())
                finally:
                    destination.unlink()

    def test_invalid_arguments_do_not_start_any_checkout(self):
        for argument in ("unknown", "--force", "../hop-alpha"):
            with self.subTest(argument=argument):
                self.assertIn("Unbekanntes Repository",
                              self.run_script("hop-alpha", argument, code=2))
                self.assertFalse((self.workspace / "hop-alpha").exists())

    def test_help_does_not_checkout(self):
        self.assertIn("Aufruf:", self.run_script("--help"))
        self.assertFalse((self.workspace / "hop-alpha").exists())

    def test_invalid_inventory_does_not_start_any_checkout(self):
        for contents in ("", "hop-alpha\nhop-alpha\n", "hop-alpha\n../outside\n",
                         "hop-alpha\n\n"):
            with self.subTest(contents=contents):
                self.inventory.write_text(contents)
                self.run_script(code=2)
                self.assertFalse((self.workspace / "hop-alpha").exists())

    def test_missing_inventory(self):
        self.inventory.unlink()
        self.assertIn("repositories.txt fehlt", self.run_script(code=2))

    def test_last_inventory_line_without_newline(self):
        self.inventory.write_text("hop-alpha")
        self.run_script()
        self.assertTrue((self.workspace / "hop-alpha" / ".git").is_dir())

    def test_continues_after_dirty_repository(self):
        self.run_script()
        path = self.workspace / "hop-alpha" / "data.txt"
        path.write_text("keep local work\n")
        head = self.advance("hop-beta")
        self.run_script(code=1)
        self.assertEqual(path.read_text(), "keep local work\n")
        self.assertEqual(self.git(self.workspace / "hop-beta", "rev-parse", "HEAD"), head)

    def test_continues_after_clone_failure(self):
        remote = self.remotes / "hop-alpha.git"
        remote.rename(self.remotes / "hop-alpha.offline")
        self.run_script(code=1)
        self.assertFalse((self.workspace / "hop-alpha").exists())
        self.assertTrue((self.workspace / "hop-beta" / ".git").is_dir())

    def test_continues_after_fetch_failure(self):
        self.run_script()
        head = self.git(self.workspace / "hop-alpha", "rev-parse", "HEAD")
        (self.remotes / "hop-alpha.git").rename(self.remotes / "hop-alpha.offline")
        beta_head = self.advance("hop-beta")
        self.run_script(code=1)
        self.assertEqual(self.git(self.workspace / "hop-alpha", "rev-parse", "HEAD"), head)
        self.assertEqual(self.git(self.workspace / "hop-beta", "rev-parse", "HEAD"), beta_head)


if __name__ == "__main__":
    unittest.main()
