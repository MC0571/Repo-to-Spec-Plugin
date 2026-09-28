# Repo-to-Spec Plugin

[中文](./README.md)

> Transform a mature software repository into a highly faithful, as-complete-as-possible system specification package without binding a new implementation to the original codebase, so an independent team or coding agent can rebuild the whole product or selectively adopt capabilities, workflows, modules, and subsystems.

## Why this project exists

Mature software repositories contain more than code. They encode product decisions, interaction rules, system boundaries, failure handling, compatibility behavior, and engineering trade-offs that have already been tested through real development and use. Rebuilding similar software without learning from that work often means rebuilding the same wheels and rediscovering the same failures.

At the same time, "open source" does not mean every repository is an appropriate implementation base for a new project. Licenses, additional terms, and usage policies can impose different constraints. Repo-to-Spec draws on clean-room design principles to separate reusable product and engineering knowledge from the reference implementation: understand what the mature project has already solved, then restate those results as specifications that can be implemented independently.

The full project motivation, target state, and design principles are documented in [VISION.md](./VISION.md).

## What it enables

Repo-to-Spec is for teams and coding agents that want to learn from mature software without directly inheriting its implementation.

- **Rebuild a complete product independently**: recover the target product's functionality, experience, external contracts, and essential system design into development-ready specifications.
- **Adopt selected capabilities**: extract a capability, workflow, module, or subsystem as design input for an existing product, then make further product and technical choices in that new context.
- **Give coding agents self-contained development input**: implementers do not need to know that the reference repository exists, and do not need to repeat repository research, requirement recovery, or key design work while coding.

Repo-to-Spec delivers **complete specifications that can be implemented independently, recomposed, and evolved**—not code intended for copying.

## Deliverable

The final deliverable is a self-contained `SYSTEM_SPEC/` package, not a repository walkthrough or a Wiki organized around the source tree.

Depending on the target product, the package may combine assets such as:

| Design content | Typical representation |
| --- | --- |
| Product goals, capabilities, business rules, and end-to-end flows | Human-readable specifications |
| Screens, interactions, visual states, and accessibility requirements | Experience specifications, design tokens, and necessary visual assets |
| Domain, state, responsibilities, concurrency, recovery, and security design | Structured models and technical specifications |
| APIs, events, configuration, and file formats | Interface definitions, protocol contracts, and schemas |
| Edge cases and acceptance behavior | Scenarios, fixtures, test vectors, and applicable conformance assets |
| What implementations may and may not vary | Implementation-freedom and constraint declarations |

Every project does not need the same directory layout or file formats. Completeness is judged by whether, within the declared scope, an independent implementation team has enough product, experience, and technical design to begin engineering without reopening key decisions.

## Core principles

### Faithful to the target product

The specification should recover the target product's functionality, experience, interfaces, state semantics, and necessary system constraints as accurately as possible. Happy paths, failures, edge states, and feature interactions are all part of the product; a summary of major features is not enough.

### Complete design, independent implementation

Critical product and system design must be explicit, but the specification should not unnecessarily freeze the original repository layout, internal symbols, framework, private data structures, or incidental module boundaries. Different teams may choose different implementations as long as they satisfy the same normative product results and constraints.

### The final package is self-contained

Implementers receive only the system specification package. They should not need access to the reference repository or be told to inspect source code to resolve unspecified behavior. Investigation can contain unresolved questions, but implementation-blocking questions cannot be presented as a final deliverable.

### Tools serve the deliverable

File search, tests, runtime observation, and optional tools such as GitNexus, CodeStory, Serena, or OpenDesign are implementation aids. They do not define the product, and users should not need to assemble a particular external toolchain before Repo-to-Spec can provide value.

### Efficiency means eliminating repeated upstream work

The goal is not to maximize investigation records. It is to prevent the next team from repeating repository study, requirement recovery, experience design, and key system design. Internal traceability and validation are useful only insofar as they improve the deliverable or reduce downstream rework.

## Working model

```text
Mature repository and available product context
                    ↓
               Repo-to-Spec
                    ↓
       Complete system specification package
                    ↓
 Independent team or coding agent with no repository access
                    ↓
 Different internal implementations, same normative product result
```

The plugin works backward from the final handoff: understand the target product, close design gaps that would block implementation, and package the result into specification assets that humans and engineering tools can consume. Investigation strategy, orchestration, and tool selection remain implementation details of Repo-to-Spec rather than dependencies of the receiving team.

## Boundaries

Repo-to-Spec is not:

- a repository Wiki or source-summary generator;
- a tool that translates directories, classes, functions, and call graphs directly into requirements;
- a code-replication system that substitutes copied internal architecture for independent design;
- a research platform whose value is measured by evidence volume, tool integrations, or document length.

This project does not determine whether a particular repository's license, additional terms, or policies permit a specific use. It does not provide legal advice or guarantee that generated specifications or later implementations are automatically authorized. Users remain responsible for applicable licensing, contractual, and compliance requirements.

## Project documentation

- [VISION.md](./VISION.md): project motivation, target state, product commitments, and long-term design principles.
- [ARCHITECTURE.md](./ARCHITECTURE.md): execution boundaries and delivery flow for the Skill-led plugin.
- [ROADMAP.md](./ROADMAP.md): the former phased roadmap is historical; current work follows the plugin and actual validation results.
- [Design documentation](./docs/README.md): current implementation entry points, verification scope, and historical design records.
- [CONTRIBUTING.md](./CONTRIBUTING.md): contribution workflow, quality requirements, and plugin/skill format conventions.
- [AGENTS.md](./AGENTS.md): hard constraints for coding agents working in this repository.

The README is limited to public positioning and delivery boundaries. Architecture, data models, and implementation plans belong in dedicated design documents rather than being duplicated here.

## Status

The repository contains an installable plugin package with one unified Skill entry and on-demand methods for capability boundaries, recovery, UI and visual behavior, data and interfaces, implementation independence, selective adoption, and specification review. Tool guidance, specification standards, and a template are included. The host Agent performs the work; no separate runtime is required.

Package structure and metadata checks do not establish real host loading, sample specification quality, or independent consumption. See [current status and verification records](./docs/README.md) for results and uncovered areas. The former S1–S6, Cxx, M0–M6, and Axx baseline and roadmap remain historical records, not an implementation checklist.

## Install and use

The local marketplace in `.agents/plugins/marketplace.json` registers `Repo-to-Spec Local`. From the repository root, install it with Codex CLI:

```sh
codex plugin marketplace add .
codex plugin add repo-to-spec@repo-to-spec-local
```

Start a new session and invoke `$repo-to-spec`. Installation, fresh-session loading, and a sample run were verified with Codex CLI `0.158.0-alpha.2.1`; see the [run record](./docs/examples/INSTALLED-PLUGIN-VALIDATION-RUN.md). The [OpenAI plugin packaging guide](https://developers.openai.com/plugins/build/plugins) also describes installation through the desktop Plugins Directory. Desktop loading has not been tested here.

Provide the repository location, target scope, intended environment, and necessary product context. For example: “Use Repo-to-Spec to analyze the import capability in `/path/to/reference-repo` for a local desktop product. Preserve the existing user interaction, include necessary dependencies, and deliver a `SYSTEM_SPEC/` that can be implemented without the source repository.”

The [bundled static pre-check specification](./plugins/repo-to-spec/examples/skill-pack-validation/SYSTEM_SPEC/) and [initial run record](./docs/examples/SKILL-PACK-VALIDATION-RUN.md) preserve an independent-consumer review. The [fresh-session specification](./docs/examples/installed-cli-run/SYSTEM_SPEC/) and [installation run record](./docs/examples/INSTALLED-PLUGIN-VALIDATION-RUN.md) cover host loading and a missing-material case. The deeper methods were also [trialed](./docs/examples/METHOD-DEPTH-VALIDATION-RUN.md) on a separate trigger-evaluation capability, retaining the original draft, reviewed revision, and unresolved dependencies. These checks cover only narrow capabilities without graphical interfaces; the new methods have not been rerun through an installed fresh session.

## Contributing

Read [CONTRIBUTING.md](./CONTRIBUTING.md) before contributing. Coding agents modifying this repository must also follow [AGENTS.md](./AGENTS.md).

## License

This repository is licensed under the [Apache License 2.0](./LICENSE). That license does not modify the terms governing any reference repository or its contents.
