# SPDX-FileCopyrightText: 2026 Murad
# SPDX-License-Identifier: MIT
import pytest
from lore_parsers import parse_jsonl


@pytest.mark.smoke
@pytest.mark.parametrize(
    ("command", "event_name"),
    [
        ("history", "revisionHistoryEntry"),
        ("info", "revisionInfo"),
        ("commit", "revisionCommitRevision"),
        ("amend", "revisionCommitRevision"),
    ],
)
def test_revision_json_has_one_completion(new_lore_repo, command, event_name):
    repo = new_lore_repo(create_repo=False)
    repo.repository_create(offline=True)
    with repo.open_file("file.txt", "w") as output_file:
        output_file.write("Initial content\n")
    repo.stage(scan=True, offline=True)
    repo.commit("Initial revision", offline=True)

    args = ["revision", command]
    if command in ("commit", "amend"):
        with repo.open_file("file.txt", "a") as output_file:
            output_file.write("Updated content\n")
        repo.stage(scan=True, offline=True)
        args.append("Updated revision")

    output = repo.run(args, json=True, offline=True)

    assert len(parse_jsonl(output, event_name)) == 1
    completions = parse_jsonl(output, "complete")
    assert [entry["status"] for entry in completions] == [0], completions
