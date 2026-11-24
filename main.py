# Say What Actually Broke — make.fun bounty
# u-po-pu-say-what-actually-broke-a2c153b5
#
# The program writes one line of software error copy (1-200 characters)
# to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. brutal truth: names the real cause plainly, no corporate fog
#   2. funny on the first read, with a real turn / fresh angle
#   3. error-copy voice: reads like something a dialog box could say
#   4. tight: one complete line, no wasted setup, lands by the last word
#   5. specific and vivid: a concrete detail, not "something went wrong"
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: truth 10, funny 9, voice 10, tight 9, vivid 9 = 47
    ("Your password is correct. The account it unlocks was deleted in "
     "2019. We've kept the login screen up out of politeness.",
     47),
    # score: truth 9, funny 9, voice 9, tight 8, vivid 10 = 45
    ("Your file wasn't lost. It was never saved — the autosave you trusted "
     "was just a little spinning wheel performing confidence.",
     45),
    # score: truth 9, funny 9, voice 8, tight 9, vivid 9 = 44
    ("We couldn't save your document because the disk is full — mostly of "
     "the 47 copies of this same file you saved 'just in case'.",
     44),
    # score: truth 10, funny 8, voice 9, tight 8, vivid 8 = 43
    ("The payment succeeded and the order failed. Your money is now in a "
     "queue with 14,000 other refunds, and the queue is not moving.",
     43),
    # score: truth 8, funny 9, voice 8, tight 8, vivid 9 = 42
    ("Error: we found your file. It is empty, it has always been empty, "
     "and the 3 hours you spent editing it were a dress rehearsal.",
     42),
    # score: truth 8, funny 8, voice 8, tight 8, vivid 9 = 41
    ("The upload failed: your 2 GB file met your hotel Wi-Fi, and the "
     "Wi-Fi lost. Nothing is broken except your expectations.",
     41),
    # score: truth 8, funny 9, voice 9, tight 8, vivid 7 = 41
    ("Your session expired while you were reading this message about your "
     "session expiring. Please log in again to watch it happen twice.",
     41),
    # score: truth 9, funny 7, voice 8, tight 8, vivid 8 = 40
    ("The server is fine. The problem is the cable between your router and "
     "the wall, which you unplugged to charge your phone.",
     40),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("turn it off", "have you tried", "404",
                  "it's not you", "something went wrong",
                  "please try again later")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a stock line: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what landed on disk: byte-identical to the chosen line, one
    # line only, inside the 1-200 character gate. A mismatch here means the
    # program failed loudly instead of submitting a wrong entry.
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert "\n" not in written, "entry must be a single line"
    assert 1 <= len(written) <= 200, f"entry over gate: {len(written)} chars"
    print(f"{line} ({len(written)} chars)")


if __name__ == "__main__":
    main()
