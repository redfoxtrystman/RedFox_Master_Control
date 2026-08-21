# Incident Report — RedFox Skin Studio Instruction-Following Failure

**Date:** 2026-08-20
**Project:** RedFox Skin Studio / BeamNG Web System
**Severity:** User-facing workflow failure

## Summary

The assistant failed to follow David's instructions during creation of a reusable towing-livery decal sheet.

David explicitly asked for help choosing a good ten-digit vanity phone number before the next image was generated. Instead of discussing options first, the assistant generated another image immediately.

David then repeated the request and also clarified that the graphic needed to be wider, with the colored design extending farther in both directions, especially to the right, and with the long graphic broken into four or more usable pieces rather than being shortened. The assistant again generated an image without first discussing or resolving the phone-number request. It also inserted an arbitrary different number and altered the graphic proportions contrary to the requested direction.

## Specific Failures

1. Ignored the first explicit request to help choose a ten-digit vanity phone number.
2. Generated an image before discussing the requested number options.
3. Added a different arbitrary number that David did not choose.
4. Ignored the repeated request to talk first before generating another image.
5. Interpreted "wider/longer" incorrectly and reduced/shrank the useful color-line length instead of extending it.
6. Failed to split the design into four or more long reusable graphic sections as requested.
7. Repeated the same instruction-following failure after David corrected the direction.

## Corrective Action

For this livery task, the assistant must not generate another image until the text/number choice and layout direction are discussed and confirmed.

The next design must:

- use only the phone number approved by David;
- contain no RedFox logo unless David asks for one;
- be substantially wider/longer for use on cars, trucks, wreckers, and semis;
- extend the seafoam/purple/silver graphic in both directions, with more extension to the right;
- provide at least four separate long graphic sections/pieces for reuse and placement;
- preserve enough continuous color area that David can stretch, crop, overlap, or adapt pieces to different vehicle bodies;
- avoid adding arbitrary text or numbers not approved by David.

## Process Rule Added

When David explicitly asks to discuss, choose, compare, or approve wording/numbers/layout before image generation, the assistant must stop image generation and resolve those choices first.
