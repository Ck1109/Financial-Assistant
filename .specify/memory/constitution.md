<!--
Sync Impact Report
- Version change: unratified scaffold → 1.0.0
- Modified principles: all five scaffold principle slots replaced with project-specific
  principles
- Added sections: Project Constraints; Development Workflow
- Removed sections: none
- Follow-up TODOs: RATIFICATION_DATE remains TODO because the original adoption date is unknown
-->

# Financial Assistant Constitution

## Core Principles

### I. Learning-First Delivery
Every feature MUST make the Agentic AI concepts it demonstrates understandable to a
learner. Implementations MUST expose the relevant concepts through clear structure,
small composable steps, and explanations in documentation or user-facing educational
content. A technically shorter implementation is not preferred when it obscures the
learning objective. This keeps the application useful as both a demo and a learning
resource.

### II. Fully Documented Code
All production code MUST be documented at the level needed for a new contributor to
understand its purpose, inputs, outputs, side effects, and important design decisions.
Public functions, classes, modules, configuration, and agent interactions MUST have
clear documentation. Documentation MUST be updated in the same change as the code it
describes. This prevents the learning material and the executable system from drifting
apart.

### III. Explicit Agentic Boundaries
Each agent, tool, prompt, workflow, and external integration MUST have a defined
responsibility and an explicit input/output contract. Agent decisions and tool calls
MUST be inspectable through appropriate status information, structured results, or
logs, without exposing secrets or unnecessary personal financial data. Features MUST
identify where orchestration, reasoning, memory, and tool use occur. Explicit
boundaries make agentic behavior teachable, testable, and replaceable.

### IV. Correctness and Safety for Financial Demonstrations
Financial calculations, transformations, and displayed conclusions MUST be
deterministic where the underlying inputs are deterministic and MUST preserve units,
currency, dates, and precision. The application MUST distinguish educational
demonstrations from financial advice and MUST avoid presenting fabricated, incomplete,
or uncertain data as fact. Sensitive values MUST be handled with least privilege and
MUST NOT be committed to source control. These rules protect users while keeping the
demo credible.

### V. Tested, Observable Simplicity
New behavior MUST have focused automated tests for its core contract and MUST include
integration coverage when it crosses an agent, tool, data, or external-service
boundary. Failures MUST be visible through actionable errors and appropriate
observability; silent fallbacks are prohibited. Implementations MUST use the simplest
design that satisfies the documented learning objective, and additional complexity
MUST be justified in documentation. This balances reliable demos with an approachable
codebase.

## Project Constraints

The project is a Python-based Financial Assistant intended for educational use and
demonstration. Dependencies MUST be justified by a documented learning or runtime
need. Interfaces and examples MUST use safe sample data by default. Configuration
MUST separate secrets and environment-specific values from source code. Any behavior
that depends on a model, provider, network, or external data source MUST document its
availability assumptions and failure behavior.

## Development Workflow

Every change MUST identify its learning objective, affected contracts, documentation
updates, and validation strategy. Contributors MUST review related documentation and
existing patterns before introducing new abstractions. Changes MUST pass the narrowest
relevant automated checks before broader checks are run. Reviews MUST verify tests,
documentation, safety considerations, and that agent behavior remains observable.
Demo-only shortcuts MUST be labeled as such and MUST NOT silently become production
assumptions.

## Governance

This constitution is the highest-level project guidance and supersedes conflicting
local practices. Amendments MUST be made through the constitution workflow, describe
the affected principles or sections, record the rationale, update the version and
amendment date, and preserve or explicitly revise any dependent documentation.

Versioning follows semantic versioning for governance: MAJOR denotes removal or
backward-incompatible redefinition of a principle; MINOR denotes a new principle or
materially expanded governance requirement; PATCH denotes clarification, wording, or
other non-semantic refinement. The ratification date is preserved after adoption;
the last-amended date changes whenever the constitution changes.

Each feature review and release-readiness review MUST check compliance with this
constitution, including documentation, tests, observability, and financial-safety
requirements. Exceptions MUST be written down with scope, rationale, owner, and
expiration or reassessment criteria. The constitution MUST be reviewed whenever the
project's learning goals, agent architecture, or safety posture materially changes.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): determine the original
adoption date | **Last Amended**: 2026-10-30
