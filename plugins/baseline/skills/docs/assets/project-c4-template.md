# {Project or system} architecture

## Purpose and audience

{What this document explains, for whom, and which decisions it does not own.}

## System context

{Describe the software system, its users, and external systems. Add a C4 System Context diagram when relationships are easier to understand visually.}

| Element | Type | Responsibility | Relationship or protocol |
| --- | --- | --- | --- |
| {Name} | {person or software system} | {responsibility} | {relationship} |

## Containers

{Describe independently deployable or runnable applications and data stores. In C4, a container is not necessarily a Docker container.}

| Container | Technology | Responsibility | Data owned | Interfaces |
| --- | --- | --- | --- | --- |
| {Name} | {runtime or store} | {responsibility} | {data} | {inbound and outbound} |

## Components when useful

{Add component detail only for a container whose internal boundaries materially help the intended audience. Omit this section otherwise.}

## Dynamic behavior when useful

{For a multi-step scenario, show numbered interactions and the failure path. Keep the static ownership model in the structural diagrams.}

## Deployment when useful

{Map software instances to infrastructure nodes, environments, trust boundaries, and network links.}

## Cross-cutting concerns

- Security and trust boundaries: {summary or link}
- Reliability and failure handling: {summary or link}
- Observability: {signals and ownership}
- Data and consistency: {ownership and guarantees}

## Decisions and evidence

- Governing inputs: {links}
- Accepted ADRs: {links}
- Validation evidence: {links or commands}
- Known limitations: {limitations}

<!--
Based on the C4 model by Simon Brown. Use only diagram levels that add value;
system context and container diagrams are sufficient for many teams.
Source: https://c4model.com/
Diagram guidance: https://c4model.com/diagrams
-->
