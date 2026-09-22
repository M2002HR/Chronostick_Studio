# ChronoStick Studio --- Full Repository Migration & Episode Archive Instructions

## IMPORTANT

This document replaces the previous refactor instruction.

The goal is NOT only to restructure folders.

The goal is to preserve the complete production knowledge learned from
Episode 001 and make future episodes repeatable.

Codex must refactor the repository and create a clean modular production
system.

------------------------------------------------------------------------

# Main Objective

After this migration, a future episode must follow this pipeline:

1.  Receive English source story.
2.  Rewrite into natural Spanish YouTube Shorts narration.
3.  Optimize:
    -   hook
    -   retention
    -   pacing
    -   ending
    -   CTA
4.  Generate voice externally.
5.  Receive word-level timestamps.
6.  Build shot plan from timestamps.
7.  Decide asset reuse:
    -   style
    -   world
    -   characters
8.  Create only the necessary new assets.
9.  Create final AI image/video prompts.
10. Generate clips.
11. Store renders and revisions.
12. Assemble final episode.

------------------------------------------------------------------------

# Repository Architecture

Use:

    Chronostick_Studio/

    docs/
      workflow.md
      production-rules.md
      video-rules.md
      audio-rules.md
      style-rules.md
      versioning.md
      decisions.md

    assets/
      styles/
      worlds/
      characters/
      episodes/

    prompts/
      image/
        styles/
        characters/
        worlds/
      video/
        templates/
        episodes/

    episodes/
      001-potato-france/
        source/
        script/
        audio/
        timestamps/
        plan/
        prompts/
        renders/
        final/

------------------------------------------------------------------------

# Prompt File Rule

A prompt file is ONLY the final text sent to the generation model.

It must NOT contain:

-   explanations
-   checklists
-   approval status
-   internal decisions
-   generation logs
-   research notes

Those belong in docs.

Example:

GOOD:

    clip-01-hook.md

    [only the Omni prompt]

BAD:

    clip-01-hook.md

    Purpose:
    ...
    Checklist:
    ...
    Prompt:
    ...

------------------------------------------------------------------------

# Permanent Production Rules

## Visual Style

ChronoStick:

-   detailed cinematic stick-figure historical animation
-   round off-white heads
-   tiny black eyes
-   minimal faces
-   simplified anatomy
-   thick clean outlines
-   detailed historical clothing
-   muted palette
-   controlled soft shading

Never drift into:

-   photorealism
-   realistic humans
-   CGI characters
-   anime
-   painterly art
-   whiteboard style
-   modern cartoon style

------------------------------------------------------------------------

# Character Identity Lock

A character reference sheet represents ONE exact character.

Never interpret:

-   front view
-   side view
-   expressions
-   poses

as different characters.

Mandatory identity features:

-   head shape
-   hair silhouette
-   clothing silhouette
-   colors
-   accessories

must remain visible.

Simplify background before simplifying characters.

------------------------------------------------------------------------

# Audio Rules

Permanent:

NO BACKGROUND MUSIC.

Allowed:

-   footsteps
-   cloth
-   paper
-   wood
-   object sounds
-   environment ambience

Forbidden:

-   soundtrack
-   score
-   melody
-   beat
-   orchestral music
-   musical ambience

Every video prompt must include:

"NO BACKGROUND MUSIC. Natural diegetic sound effects only."

------------------------------------------------------------------------

# Video Rules

Every AI video:

-   exactly 10 seconds
-   9:16
-   complete visual ending
-   no dependency on next clip

Pacing:

Hook: 6-8 visual beats.

Body: 4-6 visual beats.

Ending: 3-5 visual beats.

Permanent rule:

FAST EDITING + MODERATE MOTION.

Each shot:

-   one main action
-   one camera move maximum
-   limited secondary movement

------------------------------------------------------------------------

# Episode 001 Migration

Codex must create the final clean archive for:

001-potato-france

Preserve:

-   style reference image
-   world reference image
-   character references
-   generated videos
-   final assets

------------------------------------------------------------------------

# Video Prompt Archive Requirement

IMPORTANT:

The final successful Omni prompts from Episode 001 must be stored.

Create:

    episodes/001-potato-france/prompts/

Files:

    clip-01-hook.md
    clip-02-restriction.md
    clip-03-field-guards.md
    clip-04-night-theft.md
    clip-05-acceptance.md
    clip-06-ending.md

Each file must contain ONLY the final successful generator prompt.

Do not store failed attempts.

Do not store rejected versions.

------------------------------------------------------------------------

# Required Episode 001 Prompt Preservation

The following final prompt versions must be recovered from the
production conversation and placed exactly in the files above:

## Clip 01

Final successful hook prompt.

Requirements preserved:

-   fast opening
-   empty bowl hook
-   potato rejection
-   hard cuts
-   stable ending
-   no music
-   SFX allowed

------------------------------------------------------------------------

## Clip 02

Final successful restriction/researcher prompt.

Important fixes:

-   generator-facing prompt must not overload identity explanations
-   researcher reference controls appearance
-   style reference controls rendering
-   character hair is mandatory
-   no music
-   natural SFX allowed

------------------------------------------------------------------------

## Clip 03

Final successful field/guards prompt.

Requirements:

-   field near Paris
-   researcher
-   guards
-   same guard archetype
-   curiosity reaction
-   fast cuts
-   moderate motion
-   no music

------------------------------------------------------------------------

## Clip 04

Final successful night theft prompt.

Requirements:

-   night field
-   guards leave
-   villagers collect potatoes
-   suspense through editing
-   no chaotic movement
-   no music
-   SFX allowed

------------------------------------------------------------------------

## Clip 05

Final successful acceptance prompt.

Important fixes:

-   Style Master has priority.
-   Character sheets are identity sources only.
-   Characters must not be redesigned.
-   Same head/hair/clothing/colors.
-   No style drift.
-   No music.
-   Natural SFX allowed.

------------------------------------------------------------------------

## Clip 06

Final successful ending prompt.

Requirements:

-   researcher identity preserved
-   hair visible
-   no character simplification
-   final bowl payoff
-   CTA space for editing
-   no generated text
-   no music
-   SFX allowed

------------------------------------------------------------------------

# Decision Documentation

Create docs/decisions.md.

Record:

-   Style Master priority
-   Character identity lock
-   Prompt-only files
-   Git history version control
-   Fast editing + moderate motion
-   10-second complete ending rule
-   No background music
-   Natural SFX allowed
-   Generator prompts must avoid unnecessary identity metadata
-   Internal documentation and generator prompts are separate layers

------------------------------------------------------------------------

# Version Control

Do not use:

-   final
-   final2
-   final-final

Use Git history.

Media files can use:

    -r001
    -r002
    -r003

Never overwrite generated media.

------------------------------------------------------------------------

# Final Codex Task

Execute all migration tasks on master branch.

Verify:

-   repository is modular
-   Episode 001 is preserved
-   prompts are separated from documentation
-   future workflow is clear
-   all final successful Episode 001 prompts are archived
-   production rules are permanently documented

Commit:

    refactor: modularize ChronoStick production workflow and archive episode 001
