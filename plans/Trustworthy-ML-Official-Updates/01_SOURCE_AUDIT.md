# 01 — Official Source Audit

## Goal

Establish exactly what the official post-book materials contain before proposing repository changes.

Create:

`Validation/Trustworthy-ML-Official-Updates-2024-2026/source_inventory.md`

## 1. Inventory each official source

For each Tier A item record:

- source ID
- academic year / date
- institution
- title
- canonical URL
- material type: course page / slide deck / video / notebook / exercise / rubric / project brief
- accessible in full? yes / partial / no
- relationship to the 2023 book
- topics
- concrete evaluation requirements
- concrete implementation requirements
- named metrics
- named baselines
- named datasets/models
- explicit caveats
- candidate delta IDs

## 2. Recover exercise content

For Exercise 1–3, do not stop at the course-page title.

Attempt, in order:

1. public Kaggle notebook source / downloadable notebook
2. rendered notebook page
3. linked recap slides/video
4. official course description
5. if full content remains inaccessible, mark **partial** rather than reconstructing from guesses

For each exercise extract only:

- task
- data/model setup
- required methods
- required baselines
- evaluation metrics
- ablations/stress tests
- questions students must answer
- reporting requirements

Do not commit copied notebook bodies or slide decks.

## 3. Audit 2026 project and rubric material

Extract the evaluation logic behind each project example.

For example, distinguish:

- "prompt sensitivity exists" from "detect sensitivity at test time without ground truth"
- "RAG conflict resolution" from "surface/detect conflict"
- "attribution method" from "agreement/disagreement between attribution families"
- "calibration method" from "calibration degradation under shift"
- "reproduce paper" from "map where the claim holds and breaks"

Also extract rubric-level methodological requirements such as:

- appropriate baselines
- error bars / variability
- limitation analysis
- justified technical choices
- interpretation beyond scalar accuracy

## 4. Version comparison

Use the 2023/24 course page as a historical control where helpful.

For each material family classify:

- already represented in book-era course
- new/reframed in 2024/25
- new/reframed in 2026

## 5. Access limitations

Record inaccessible sources explicitly.

Do not infer missing notebook requirements from topic names.

## Gate U1

PASS only if every Tier A source has:

- an inventory row;
- access status;
- enough extracted detail to support or reject a delta, or an explicit "insufficient evidence";
- no content attributed to a source that was not actually read.
