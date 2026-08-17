---
# DESIGN.md — design tokens.
# Format: the open DESIGN.md specification — https://stitch.withgoogle.com/docs/design-md/specification
# Rules: colors are hex codes, never names; every value concrete; validate with the format's own CLI (see the spec repo).
colors:
  primary: "" # hex, e.g. "#1A73E8"
  surface: ""
  text: ""
typography:
  family: ""
  scale: [] # e.g. [12, 14, 16, 20, 24, 32]
spacing:
  scale: [] # e.g. [4, 8, 12, 16, 24, 32]
radii:
  scale: [] # e.g. [4, 8, 16]
---

## Overview

One paragraph: what this product looks and feels like, and why.

## Visual Theme & Atmosphere

The overall tone and aesthetic intent — the words a reviewer would use for a screen that belongs here.

## Colors

Each color: hex, role, usage rule. No names without hex.

## Typography

Families, the scale, weights, and where each step of the scale is used.

## Layout

Grid, breakpoints, density, spacing rules.

## Elevation & Depth

Shadow/elevation steps and what each communicates.

## Shapes

Radii and shape language, per component class.

## Components

Per component: the pattern with concrete values — never adjectives without numbers.

## Do's and Don'ts

The short list a reviewer checks first. Grows from real review findings, not speculation.

## Agent Prompt Guide

Instructions for agents building UI against this system: what to read first, what never to invent, tool-specific notes if any.
