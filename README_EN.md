# Repo-to-Spec Plugin

[中文](./README.md)

> Recover a verifiable, traceable, implementation-independent Canonical Spec from an existing code repository so an independent implementation can rebuild the system without relying on the original implementation details and can later be validated against the Spec.

## Purpose

Repo-to-Spec is for reverse specification of existing code repositories.

It focuses not on how the code is written, but on recovering from source code, tests, configuration, interface definitions, and observable behavior:

- what capabilities the system exposes;
- how inputs, outputs, and errors are defined;
- how configuration, state, and lifecycle behavior work;
- what filesystem, persistence, and network side effects exist;
- how ordering, precedence, fallback, compatibility, and security boundaries constrain behavior;
- which behaviors are confirmed by evidence and which remain ambiguous or uncovered.

The resulting specification should support an independent implementation without requiring the original repository's internal structure to be reproduced.

## Core principles

### Evidence-grounded

Material requirements in the Canonical Spec should be traceable to reviewable evidence whenever possible.

Investigation should distinguish:

- confirmed behavior;
- inference supported by consistent evidence;
- unverified assumptions;
- uncovered areas;
- conflicting evidence.

Unknown behavior should remain explicitly unknown rather than being filled in by the investigator.

### Observable behavior first

Prefer externally observable contracts, including:

- CLI, API, and protocol surfaces;
- configuration and environment variables;
- input, output, error, and exit behavior;
- state transitions and lifecycle behavior;
- filesystem, persistence, and network side effects;
- ordering, precedence, and fallback rules;
- compatibility and security boundaries;
- observable constraints such as determinism and idempotency.

### Implementation-independent

The Canonical Spec defines what must be true, not how it must be implemented.

Unless an implementation detail is itself part of a compatibility contract, the Spec should not require:

- the original repository layout;
- internal class or function names;
- private data structures;
- incidental module boundaries;
- replaceable algorithmic details;
- unnecessary technology choices.

### Coverage and closure

Specification completeness is not measured by document length.

Investigation should continuously identify:

- behavior surfaces already covered;
- areas not yet investigated;
- unresolved ambiguities;
- conflicting evidence;
- information still missing for independent implementation.

A Spec is reliable only when the important behavior and constraints are sufficiently closed.

### Spec is normative

The Canonical Spec is the normative source for behavior and constraints.

Independent implementations may use different internal designs as long as their observable behavior conforms to the same Spec.

## Working model

```text
Reference Repository
        ↓
Repository Investigation
        ↓
Evidence + Coverage
        ↓
Canonical Spec
        ↓
Spec Validation
        ↓
Conformance Evidence
```

Where:

- **Repository Investigation** locates and verifies behavior-relevant source, tests, configuration, and runtime evidence;
- **Evidence + Coverage** records evidence sources, confidence, coverage, and unresolved items;
- **Canonical Spec** captures implementation-independent behavior, interfaces, constraints, and boundaries;
- **Spec Validation** checks completeness, clarity, consistency, verifiability, and implementation independence;
- **Conformance Evidence** provides reviewable evidence for validating a later implementation.

## Boundaries

Repo-to-Spec is not intended to:

- reproduce the reference repository's internal architecture;
- restate the code structure as documentation;
- prescribe directories, modules, or algorithms for an independent implementation;
- fill specification gaps with unverified assumptions;
- treat implementation plans or task breakdowns as part of the Canonical Spec.

## Contributing

Before contributing, read:

- [CONTRIBUTING.md](./CONTRIBUTING.md) for repository-wide development and quality requirements;
- [AGENTS.md](./AGENTS.md) for Coding Agent execution constraints in this repository.

## License

This repository does not currently contain a LICENSE file. Do not assume an open-source license grant until one is explicitly added.
