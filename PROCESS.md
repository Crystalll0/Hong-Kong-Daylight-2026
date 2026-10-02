# Process

<!-- Same as assignment 1, same honesty. Which tools you used and for what; one
thing you kept and why it was good; one thing you rejected and why it was wrong.
"I did not use any" is fine if it is true.

If a model wrote most of plot.py, which is likely and allowed, the interesting part
is what you had to correct: did it invent a column name, use pandas where a list
would do, silently drop the rows it could not parse? -->

## Tools

I used Codex to help me understand the assignment, find the data source and check the coding format. I chose the topic of changing daylight duration in Hong Kong and suggested adding sun icons and sky colours during an earlier prototype discussion.

Before starting work in this repository, I asked Codex to act as a teacher and prepare a step-by-step tutorial. It provided explanations and code examples, including complete scripts. I used this guidance to understand the structure and identify which parts to enter, replace or add in VS Code.

When errors appeared, I tried to make corrections. But if the problem still remained, I asked Codex to help identify the cause. One problem turned out to be simpler than I expected: I had forgotten to save the edited file before running it...

## Problems and corrections

Initially, I was still running the template's temperature download script rather than the replacement solar-time script. I corrected the file contents and saved the changes.

While editing `fetch.py`, I also encountered an indentation error. After replacing the code and correcting the indentation, the script ran successfully.

When I first ran `plot.py`, I had not saved the replacement code. Python therefore ran the old template and tried to read the temperature CSV. Saving the edited file and running it again successfully generated the daylight chart.

These problems helped me understand the order of the steps: edit the file, save it, run the program, commit the changes and push them to GitHub.


## Kept

I kept the simple line chart as the first committed visual draft. It clearly shows the annual change in daylight duration and provides a starting point for comparing later designs.

## Rejected

I replaced the template's temperature example because it did not match my chosen phenomenon.

I also adopted the term "daylight duration" rather than "sunshine duration," following a clarification in the discussion with Codex. Subtracting sunrise from sunset does not measure the actual duration of bright sunshine.

## Next iteration

The current chart shows how long daylight lasts each day, but does not show sunrise and sunset times separately.

Next, I plan to compare a solar-time panel with the daylight-duration curve and record which design choices I actually keep or reject, along with my reasons.


# Daily Report


## 29 September 2026 — Data and the first chart

I downloaded the Hong Kong Observatory's 2026 sunrise, solar transit and sunset CSV. Running the download script again confirmed that it reused the saved file rather than downloading it repeatedly.

I ran the inspection script to check all 365 daily records. The first day's daylight duration was 648 minutes. The shortest duration was 646 minutes, the longest was 810 minutes, and the difference was 164 minutes.

Then I generated a simple line chart using the locally saved data. I committed the data and inspection script before committing the first chart, preserving two separate stages in the repository history.

## 30 September 2026 — Solar times and opacity comparison

I replaced the single-chart layout with two vertically arranged panels. The upper panel shows sunrise, solar noon and sunset, while the lower panel retains the daylight-duration curve. Both panels share the month axis.

This change addresses a limitation of the first version: it showed how long daylight lasted but did not show the separate sunrise and sunset times. Solar noon uses the published TRAN. values rather than a fixed 12:00.

I ran the updated script and compared BAND_ALPHA values of 0.7 and 0.25. The higher opacity made the daylight area more prominent, while the lower opacity produced a lighter background.

Codex recommended 0.7 to emphasise the daylight band, but I preferred the lighter appearance of 0.25 and kept that version. This makes the filled area less prominent, which is a trade-off I accepted.

The data and calculations were unchanged during the opacity comparison.

## 1 October 2026 — Sky colours and sun icons

Today, I wanted to improve the chart's appearance, so I discussed possible changes to the existing code with Codex. And with the help by Codex, I success created the new version with gradient and three sun icons to the solar-time panel to make the table clearer. I retained the daylight-duration curve below it and kept the opacity at 0.25, following my preference from the previous iteration.

The gradient follows the daily sunrise, solar noon and sunset times. The colours and intermediate transitions are design choices, not weather measurements or calculated twilight boundaries.

I compared different color to present the solar noon session. After viewing both versions, I chose to restore the earlier pale-gold version and regenerated the image. I preferred its warmer appearance while keeping the overall colours soft.

During editing, I accidentally entered the colour value in the terminal. It was not a command; it shoulded be belong in plot.py. The final plotting run completed successfully.

This iteration changed the presentation to help distinguish sunrise, solar noon and sunset. It did not change the original data or the calculation of daylight duration.

## 2 October 2026 — Final Version

Today, I reviewed the project before submission. I ran `uv run --offline plot.py` successfully, and the script regenerated the figure using all 365 locally saved daily records. This confirmed that plotting could run without downloading data again, with the required dependencies already installed.

The assignment-check command initially failed because the connection timed out while downloading the checker. I later retried the command, and all automated checks passed. The results confirmed that the README displayed the image, the scripts declared their dependencies, the data and output image were included, and the repository contained six commits across three days.

I also updated the README to describe the final version rather than a planned next iteration. The final figure retains the two-panel layout, sun icons, a pale-gold sky gradient and an opacity of 0.25.