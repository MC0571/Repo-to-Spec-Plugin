# Repo-to-Spec Plugin

[中文](./README.md)

> Derive a verifiable, traceable, implementation-independent Canonical Spec from an existing code repository. Investigators retain source evidence and deliver a specification without the reference repository's identity, source code, or investigation records. Implementers can then rebuild the needed capabilities or adopt selected capabilities in another system without knowing the reference repository exists, and validate the chosen scope against the Spec.

## Purpose

Repo-to-Spec is for reverse specification of existing code repositories, especially where license terms and information boundaries require careful handling.

It investigates source code, tests, configuration, interface definitions, and observable behavior to recover:

- what capabilities the system exposes;
- how inputs, outputs, and errors are defined;
- how configuration, state, and lifecycle behavior work;
- what filesystem, persistence, and network side effects exist;
- how ordering, precedence, fallback, compatibility, and security boundaries constrain behavior;
- which behaviors are confirmed by evidence and which remain ambiguous or uncovered.

Investigators retain evidence for review; the Canonical Spec delivered to implementers contains only the behavior and constraints needed for implementation. Implementers may rebuild the whole system or select only the capabilities they need. If required compatibility information would reveal the source, that limitation should be stated explicitly.

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

The Canonical Spec defines what must be true, not how it must be implemented. Source structure and internal architecture are investigation evidence that can reveal behavior, interfaces, and constraints.

If an architectural feature is itself an observable behavior, compatibility requirement, or security boundary, the Spec should include it when supported by evidence. Otherwise, the Spec should not require these implementation choices:

- the original repository layout;
- internal class or function names;
- private data structures;
- incidental module boundaries;
- replaceable algorithmic details;
- unnecessary technology choices.

The delivered specification should not contain the reference repository's identity, source code excerpts, or evidence records used only for investigation.

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
Evidence + Coverage (investigation side)
        ↓
Canonical Spec
        ↓
Spec Validation
        ↓
Delivery to Implementers
        ↓
Rebuild or Selective Adoption
        ↓
Conformance Evidence
```

Where:

- **Repository Investigation** locates and verifies behavior-relevant source, tests, configuration, and runtime evidence;
- **Evidence + Coverage** records evidence sources, confidence, coverage, and unresolved items on the investigation side;
- **Canonical Spec** captures implementation-independent behavior, interfaces, constraints, and boundaries;
- **Spec Validation** checks completeness, clarity, consistency, verifiability, and implementation independence;
- **Delivery to Implementers** provides only the validated specification, without the reference repository or investigation records;
- **Rebuild or Selective Adoption** implements the full specification or a chosen set of capabilities independently;
- **Conformance Evidence** provides reviewable evidence for validating the chosen scope of a later implementation.

## Boundaries

Repo-to-Spec analyzes source code and architecture to recover behavior, interfaces, and boundaries that must be preserved, but is not intended to:

- require a new implementation to reproduce the reference repository's internal architecture;
- turn source directories, modules, classes, or call relationships directly into specification requirements;
- prescribe directories, modules, or algorithms for an independent implementation;
- fill specification gaps with unverified assumptions;
- treat implementation plans or task breakdowns as part of the Canonical Spec.

For example, investigating a configuration module should recover confirmed configuration sources, precedence, and error behavior, rather than merely list the module's responsibilities.

This project does not determine whether a particular repository's license permits a given use, or guarantee that a specification or implementation is automatically authorized for use.

## Contributing

Before contributing, read:

- [CONTRIBUTING.md](./CONTRIBUTING.md) for repository-wide development and quality requirements;
- [AGENTS.md](./AGENTS.md) for Coding Agent execution constraints in this repository.

## License

This repository is licensed under the [Apache License 2.0](./LICENSE). This license does not change the terms governing any reference repository or its contents.
