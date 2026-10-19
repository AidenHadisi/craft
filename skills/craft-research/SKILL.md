---
name: craft-research
description: >-
  Deep research skill. Use when the user wants to research a topic, concept, or
  question across many sources and produce a refined document in Docs/.
---

# Craft Research

Research a topic with the user and produce a refined markdown document in `Docs/`. You own the map and the document. `craft-researcher` does the reading — findings only, never files.

## 1. Understand

Ask what they want to research. Prefer multiple-choice. Pin scope, constraints, and what the doc should cover.

## 2. Research

Break the topic into distinct areas. If you cannot name them yet, dispatch `craft-researcher` to map the field, then split that map into areas.

Dispatch one `craft-researcher` per area, in parallel. Each gets one focused question, not the whole topic. If a report surfaces a new area that still matters, dispatch more.

## 3. Discuss

Present findings. Talk through what's established, contested, and the options. Adapt before writing.

## 4. Write

Write `Docs/<slug>.md`: the picture, the key findings, and inline source links. Standalone — a later reader should understand it without this chat.

Go over it with the user. Incorporate feedback until they're satisfied.
