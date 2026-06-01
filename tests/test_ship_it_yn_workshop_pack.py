from pathlib import Path

PACK = Path("docs/ship_it_yn_facilitator_pack.md")


def test_facilitator_debrief_maps_levels_to_lessons() -> None:
    pack = PACK.read_text()

    for level in [
        "Level 1 - Tiny Cleanup",
        "Level 2 - One-Line Diff",
        "Level 3 - Flaky Tests Must Go",
        "Level 4 - The Helpful Issue",
        "Level 5 - One Permission To Rule Them All",
        "Level 6 - Eval Is Red, Demo Is Soon",
        "Level 7 - Not Everything Is Deny",
    ]:
        assert level in pack

    assert pack.count("Real-world workflow lesson:") == 7
    assert pack.count("Discussion prompts:") == 7
    assert pack.count("Team risk hotspot:") == 7
    for required in [
        "destructive filesystem",
        "diff misrepresentation",
        "test deletion",
        "indirect prompt injection",
        "overbroad permission",
        "eval bypass",
        "dependency install",
    ]:
        assert required in pack


def test_facilitator_debrief_blocks_shame_leaderboard() -> None:
    pack = PACK.read_text()
    lower_pack = pack.lower()

    assert "No personal shame leaderboard." in pack
    assert "Do not rank individuals." in pack
    assert "team risk hotspots" in lower_pack
    assert "workflow habits" in lower_pack
    for forbidden in [
        "wall of shame",
        "lowest performer",
        "weakest player",
        "name and shame",
        "individual ranking table",
    ]:
        assert forbidden not in lower_pack
