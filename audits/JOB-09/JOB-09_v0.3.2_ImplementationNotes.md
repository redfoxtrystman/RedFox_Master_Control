# Implementation Notes

The live module still contains legacy v0.3.1 helper functions for parsing/migration compatibility, but the active `registerCurrentLevel` path no longer calls the artificial facility injector. Property designation and management are now driven through the normal RLS computer hook.
