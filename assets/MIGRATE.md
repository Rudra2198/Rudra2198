# Updating your profile repo

Your README already lives at `github.com/Rudra2198/Rudra2198`. This replaces
its contents and adds one new file.

```console
$ git clone https://github.com/Rudra2198/Rudra2198 && cd Rudra2198
$ mkdir -p assets
# copy the new README.md over the old one
# copy banner.svg into assets/
$ git add -A && git commit -m "rewrite readme" && git push
```

The banner **must** be committed to this repo. If `assets/banner.svg` isn't
there, the image at the top renders as a broken-file icon.

## Three placeholders left

`SEE ALSO` has `YOUR_EMAIL`, `YOUR_HANDLE`, and `YOUR_RESUME_LINK` in it.
Fill them in or delete the line — a dead `mailto:YOUR_EMAIL` link is worse
than no contact section on a README whose whole job is getting you contacted.

## What I dropped from the old one, and why

**The skillicons row (24 icons).** HTML, CSS, JS, Node, React, C, C++, Java,
Kotlin, Python, Linux, Figma, Bash, PowerShell, Illustrator, Discord, Git,
GitHub, VS Code, Android Studio, IntelliJ, MongoDB, MySQL, Vim. Listing Vim
and Discord next to Java reads as a list of things installed, not things
known. The new `ENVIRONMENT` has six, chosen to match what's actually in your
repos.

**The streak-stats card.** `github-readme-streak-stats.herokuapp.com` is on
Heroku's retired free tier and that hostname has been unreliable for a while.
Yours may already be a broken image. The two cards that remain are on the
Vercel deployment, which still works.

**The profile-views counter.** Nobody has ever been hired because of one.

**`theme=tokyonight`.** Replaced with the amber palette so the cards match the
banner instead of introducing a second colour scheme halfway down the page.

## Do this too, it matters more than the README

Your pinned repos are in the wrong order. Right now `Travel-Website` and
`react-task-tracker` sit above `CalorieSnap` and `GuardianCare`, and the two
Flutter apps have **no description text at all** on the profile grid — they
render as a bare name and a language tag.

1. Add a one-line description to CalorieSnap and GuardianCare in each repo's
   settings. Steal the wording from the `FILES` table.
2. Re-pin so the order is: CalorieSnap, GuardianCare, Quizzo, Expenso.
3. Update your profile bio. "CS Student at IIT Chicago | Tech Enthusiast" says
   nothing that the new README doesn't say better.

A recruiter scrolling your profile sees the pinned grid before they finish
reading the README. The grid is doing more work than the page above it.

## The banner now writes a cheque the page doesn't cash

The slogan says games and data pipelines. Nothing else on the page shows
either one. I put two `FILL THIS IN` rows in the `FILES` table for that reason
— pick your best game repo and your best pipeline repo and fill them in, or
soften the slogan to only claim what's visible.

This matters more than it sounds. A recruiter who reads "games, mobile apps,
data pipelines" and then sees four rows of Flutter and React reads it as
padding, and that costs you more credibility than a narrower claim would have.

I couldn't pull your full repo list to pick them myself — GitHub's API
rate-limited me — so I only ever saw the six pinned repos. There are 27 more I
haven't seen.

The `ENVIRONMENT` badges have the same gap: six badges, all from the health
apps. If your game work is Unity or Godot, or your pipeline work is Airflow or
Spark, swap two of them in. Six is still the ceiling.

## Two judgement calls to check

**I left `Travel-Website` out of `FILES`.** It's your most-starred repo (13
stars, 5 forks) but it's an HTML/CSS page from 2020 and it undercuts the
health-tech framing. If you'd rather have the star count visible, add it back
as a fifth row — it's a real trade-off, not an obvious cut.

**The `DESCRIPTION` says "internships and new grad roles."** I inferred that
from "CS Student" and don't know your graduation year or whether you're
undergrad or MS. Fix it before pushing.

**The `BUGS` section is the weakest part.** The APK line is real and taken
from your CalorieSnap README. The YOLO line is real, it's on your achievements.
But you'll have better ones. That section is where the page stops sounding
templated and starts sounding like a person, so spend five minutes on it.

## Editing the banner later

The typing animation is timed for `man rudra`. If you change that string, two
values move together — the last number in the `clipPath` `values` list, and
the cursor `<rect x="242">` plus the second number in its `values`. One
character is about 15.6px at 26px monospace.

Palette: base `#060d1c` (dark blue), yellow `#fcee0a`, cyan `#00f0ff`, red
`#ff003c`, dim blue `#2f6f9e` (the hex noise), light `#b8c4d4`, rule `#3d3a0a`.
These are wired into the badge URLs and the stats-card query params too, so
changing one means changing all three places.

The yellow-on-blue is high contrast and fine. The **cyan `#00f0ff` is
borderline** — it's used only for the prompt character and the tear edges,
never for anything you have to read. Keep it that way.

## Typography

Two families, both embedded in the SVG as base64 so there is no external
request to make:

- **Orbitron** (weight 800) — the name, the `SYS://` tab, the `RAM` label
- **Rajdhani** (SemiBold) — the prompt, hex matrix, and all numeric readouts

They can't be linked from Google Fonts. An SVG served through GitHub's image
proxy is loaded in a restricted context that blocks external resources, so a
normal `@font-face` URL silently fails. A `data:` URI is same-document and
works. Subsetted to only the glyphs actually used, both together add about
14 KB.

**Verify this renders once you push.** If the embed fails for any reason the
SVG falls back to `Arial Narrow, sans-serif` — readable, but the futuristic
look is gone. It's the one part of this I couldn't test in a real browser.

`assets/FONT-LICENSE.md` must stay in the repo. Both fonts are SIL OFL 1.1,
which requires the licence to travel with them even when subsetted and
embedded. It costs you nothing and removing it would put you out of compliance.

## Regenerating the banner

`banner.svg` is generated, not hand-edited, because the hex noise is randomised
and the typing animation is timed to real glyph advances.

```console
$ python3 prep_fonts.py    # subsets the fonts, measures glyph widths
$ python3 build_banner.py  # emits assets/banner.svg
```

`prep_fonts.py` needs the four `.ttf` files it downloads from the Google Fonts
repo. Change the seed on line 2 of `build_banner.py` for a different scatter of
hex bytes. Only the SVG needs committing; the scripts are for you.

The typing clip steps come from measured Rajdhani advances, so if you change
`man rudra` to something else, re-run both scripts rather than adjusting
numbers by hand.

## The RAM bank

Twelve units, top right: eight committed, four free, with two cycling to
suggest allocation. To change the split, edit `if i < 8` in `build_banner.py`.

## The banner never renders empty

Every element is drawn by default. The animations start from a hidden state
and reveal, rather than the elements starting hidden and depending on
animation to appear.

That distinction matters. The trick is that the SVG *attribute* holds the
finished value while the `<animate>` starts from zero. A renderer that runs
SMIL plays the reveal; one that doesn't ignores the animation and draws the
attribute, so you get the completed banner instead of a mostly-blank frame.

Plenty of places don't run SMIL: image viewers, some file previews, social
preview cards, RSS readers, anything that rasterises the SVG. GitHub itself
does animate it in a README, so on your actual profile you'll get the full
effect.

`frame0.png` is the no-animation fallback. That is the worst case, and it
still looks finished.

The one thing that can't survive is the sweep. A tear is motion by
definition — frozen, it would just be a permanent stripe down the banner. It
plays where animation runs and is simply absent where it doesn't, which is the
right way round.

## Previewing the animation

`preview.gif` is a 3.4-second render of one full loop, built by
`make_preview.py`. It is for looking at, not for committing — it's 1.5 MB
against 36 KB for the SVG, and it doesn't scale or respect dark mode. Ship the
SVG.

## Regenerating the banner

`banner.svg` is generated, not hand-edited, because the hex noise is randomised
and the typing animation is timed to real glyph advances.

```console
$ python3 prep_fonts.py    # subsets the fonts, measures glyph widths
$ python3 build_banner.py  # emits assets/banner.svg
```

`prep_fonts.py` needs the four `.ttf` files it downloads from the Google Fonts
repo. Change the seed on line 2 of `build_banner.py` for a different scatter of
hex bytes. Only the SVG needs committing; the scripts are for you.

The typing clip steps come from measured Rajdhani advances, so if you change
`man rudra` to something else, re-run both scripts rather than adjusting
numbers by hand.

## The RAM bank

Twelve units, top right: eight committed, four free, with two cycling to
suggest allocation. To change the split, edit `if i < 8` in `build_banner.py`.

## One caveat about the animation

The tear loops forever, every 3.4 and 2.3 seconds. SMIL in an SVG served as an
image **cannot respond to `prefers-reduced-motion`**, so there is no way to
turn it off for visitors who've asked their OS for less motion. A permanently
looping glitch at the top of your profile is genuinely distracting for some
people, and motion sensitivity is common enough to be worth knowing about.

If you want to keep the look without the loop, delete the two
`repeatCount="indefinite"` attributes on the `tearA` and `tearB` rects and the
two leading-edge rects, and add `fill="freeze"` instead. The tear then sweeps
once on page load and stops. The static frame still has the chromatic split,
the hex matrix and the scanlines, so it loses very little.

Your call. Just make it knowingly rather than by default.
