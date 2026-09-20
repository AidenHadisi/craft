---
name: craft-quick
description: Quickly plan and build a small, clear feature with one architecture approval and automated checks. Use when the user says "craft quick" or wants a lightweight alternative to the full craft workflow.
---

# Craft Quick

Move from a clear request to tested code with one user gate. Keep everything in the conversation: no spec, plan file, live testing, branch, commit, or PR.

## 1. Explore

Quickly inspect the relevant code, neighboring examples, conventions, and available check commands. Delegate reading when useful, but keep exploration proportional to the task.

Ask questions only when a missing product decision or constraint would materially change the implementation. Otherwise use the simplest repo-consistent interpretation.

## 2. Architecture

Propose the work as numbered tasks in dependency order. Each task is a title plus a short body: files to change, sibling to mirror, and a schema, signature, or pseudocode block when the coder would otherwise guess.

Do not write Components, Seams, Key decisions, or Slices.

Hold the design to the Standards in [architecture](references/architecture.md) and use that file's Write format. Do not create a plan file.

## 3. Critic loop

Dispatch a fresh `craft-critic` with the request, repo findings, and proposed tasks.

- **Holds:** continue.
- **Better design:** adopt it unless there is a concrete reason not to. Revise the tasks and dispatch a fresh critic.

If the loop cannot converge after three critiques, show the disagreement and ask the user.

## 4. Approve

Show the task list and summarize the alternatives the critic rejected. Let the user decide whether to approve it or make changes.

Do not build until the user approves.

## 5. Build and test

Dispatch one `craft-coder` with the approved tasks, files, repo conventions, and automated check commands. The coder implements the whole change and runs the checks.

If the coder reports blocked, show the blocker and ask the user. Otherwise report:

- what changed
- which checks ran and their results
- any deviations or remaining risks

Stop. Do not live-test, review, polish, commit, create a branch, push, or open a PR.
