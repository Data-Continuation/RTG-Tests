# RTG TV/TVC Math-Solver Authority Execution Bundle

Generated: `2026-06-02T04:58:26Z`

## Purpose

This bundle replaces the direct-token execution plan with a StegVerse-native authority path.

RTG should not own the raw GitHub workflow dispatch credential.

Instead:

```text
RTG requests authority
TV/TVC validates and grants authority
RTG validates the authority receipt
RTG dispatches only under that authority boundary
```

## Required External Authority

```text
StegVerse-Labs/TV
StegVerse-Labs/TVC
```

## Runtime Token Boundary

If actual dispatch is executed, the token should be supplied as a TV/TVC-brokered output:

```text
TV_TVC_MATH_SOLVER_DISPATCH_TOKEN
```

not as an RTG-owned long-lived repo secret.

## Runtime Switch

```text
RTG_SOLVER_EXECUTE=true
```

Without `--execute` or `RTG_SOLVER_EXECUTE=true`, the dispatch layer produces an authority-bound dispatch packet without calling GitHub.
