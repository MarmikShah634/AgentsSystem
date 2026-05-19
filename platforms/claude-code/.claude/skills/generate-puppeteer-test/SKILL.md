---
id: generate-puppeteer-test
category: testing
owner_agent: tester
inputs:
  - feature_url
  - acceptance_criteria
outputs:
  - puppeteer_script_path
requires_plan: true
emits_confidence: true
---

# Skill: generate-puppeteer-test

## Task

Author a Puppeteer script under `puppeteer/tests/<feature>.test.js` that
exercises the feature end-to-end via a real browser.

## Required coverage

- Golden path (success scenario).
- At least one edge case (validation error, empty state, or unauthorised
  access).

## Implementation

Use the helpers exported by `puppeteer/helpers/`. Run via
`node puppeteer/runner.js <script>`.

## Stop condition

Script passes against a running dev server and fails with a clear message
when the feature is mutated.
