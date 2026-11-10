# Reconstructed frozen constant predictors

`CONSTANT_MODEL_STATE.json` resolves scalar prediction state for 117 expanded-candidate reference tasks: 54 training means, 9 training frequencies, and 54 exact zero-change references. Each state retains its original task ID, input version, target, horizon, fold, source line/blob, original decimal literal, binary64 representation, mathematical mapping, and SHA256.

The values come from the original full-precision `source/all_model_fold_metrics.csv`. The presentation table rounds these statistics and is not used to reconstruct values. Original Julia producer assignments and the candidate wrapper were inspected and Git-blob verified. The original binary probability clamp is retained as an explicit source transformation.

This is reconstruction of frozen constants, not recovery of trained weights or a refit. No training data were recomputed. No training mean substitutes for any of the 54 median references; the original checkpoint left those unresolved. The supplemental RECOVERY_BINDINGS.json now restores 22 exact zero medians and retains 32 nonzero-scalar precision dependencies. All other missing or unverified states remain unchanged.

The resolution is supplemental. Original recipes, evidence, broad instance IDs and their execution-disabled state are unchanged. A runtime adapter must bind these constants explicitly; no feature/provider availability or platform support is asserted. Causal opportunities, target deadlines, execution inputs and actual platform fills remain necessary.

`CONSTANT_MODEL_STATE_RESOLUTION.json` records provenance, precision differences, 63 saved-metric identity checks, remaining dependencies, and hashes. Reproduce with `python machine/build_constant_model_state.py`.
