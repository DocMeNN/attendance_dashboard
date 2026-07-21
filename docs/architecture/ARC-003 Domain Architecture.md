# Online Bible Study Attendance and Participation Analytics Platform

# ARC-003

# Domain Architecture

---

## Document Information

| Property | Value |
|----------|-------|
| Document ID | ARC-003 |
| Title | Domain Architecture |
| Version | 1.0 |
| Status | Draft |
| Classification | Public |
| Owner | TechAndMe |
| Author | TechAndMe |
| Reviewer | Chief Architect |
| Approver | Chief Architect |
| Effective Date | July 2026 |
| Last Updated | July 2026 |

---

> **Building Better Software.**
>
> **Building Better Engineers.**

---

# Table of Contents

1. Preamble
2. Purpose
3. Scope
4. Role of the Domain Layer
5. Domain Principles
6. Domain Concepts
7. Domain Model
8. Domain Entities
9. Related Documents
10. Revision History
11. Closing Reflection

---

# Preamble

The Domain Layer represents the core knowledge of the Online Bible Study Attendance and Participation Analytics Platform.

It defines the concepts, rules, relationships, and analytical behaviour that give meaning to the data processed by the platform.

While the Presentation Layer displays information and the Infrastructure Layer processes technical inputs, the Domain Layer determines what the information means.

The Domain Layer is therefore the intellectual centre of the platform.

It transforms raw participation data into meaningful domain concepts such as:

- sessions;
- participants;
- attendance;
- participation;
- activities;
- engagement;
- recognition;
- analytics.

The Domain Layer must remain independent of presentation technologies, databases, file formats, external services, and AI providers.

---

# 1. Purpose

The purpose of this document is to define the architecture of the Domain Layer.

It establishes:

- the core domain concepts;
- domain entities;
- value objects;
- domain services;
- business rules;
- analytical responsibilities;
- relationships between domain concepts.

This document serves as the authoritative architectural reference for the platform's core business and analytical logic.

---

# 2. Scope

This document covers the Domain Layer of the platform.

It includes:

- Domain entities
- Value objects
- Domain models
- Business rules
- Domain services
- Analytical concepts
- Domain relationships

It does not define:

- user interface implementation;
- file parsing;
- database implementation;
- AI provider integration;
- deployment infrastructure.

Those concerns are documented separately.

---

# 3. Role of the Domain Layer

The Domain Layer defines the meaning of the platform.

Its primary responsibility is to answer questions such as:

- What is a study session?
- What constitutes attendance?
- What constitutes participation?
- What activities can a participant perform?
- How is engagement measured?
- How is recognition determined?
- How are analytical metrics calculated?

The Domain Layer transforms technical data into meaningful domain knowledge.

---

# 4. Domain Principles

The Domain Layer follows the following architectural principles.

## Technology Independence

Domain logic shall not depend upon external frameworks or infrastructure technologies.

---

## Business Rule Centralisation

Business rules shall be defined within the Domain Layer rather than scattered throughout the application.

---

## Explicit Domain Language

Domain concepts shall be represented using clear and meaningful names.

---

## Deterministic Behaviour

Given the same valid input, domain operations should produce the same result.

---

## Separation of Concerns

Entities, value objects, domain services, and analytical operations shall have clearly defined responsibilities.

---

## Testability

Domain logic should be independently testable without requiring:

- a database;
- a user interface;
- an external API;
- an AI provider;
- a network connection.

---

# 5. Core Domain Concepts

The platform is built around several central domain concepts.

## Study Session

A defined period of Bible study activity.

A session may contain:

- a date;
- a topic;
- a collection of messages;
- participants;
- attendance events;
- activity events.

---

## Participant

An individual identified within the study community.

A participant may:

- attend sessions;
- participate in discussions;
- perform activities;
- contribute insights;
- receive recognition.

---

## Attendance

Represents a participant's presence or participation in a defined study session.

Attendance is an analytical concept rather than merely a message count.

---

## Participation

Represents meaningful involvement in study community activities.

Participation may include:

- attendance;
- responses;
- scripture contributions;
- questions;
- insights;
- prayer participation;
- other recognised activities.

---

## Activity

Represents a specific type of participant contribution.

Activities are classified according to the platform's activity taxonomy.

---

## Engagement

Represents the degree and pattern of participation over time.

Engagement may be analysed at:

- participant level;
- session level;
- community level.

---

## Recognition

Represents the identification of meaningful participation patterns.

Recognition may include:

- participation milestones;
- consistent attendance;
- contribution achievements;
- activity-based recognition.

---

# 6. Domain Model Overview

The high-level domain model is represented below.

```text
Participant
     │
     ├──────────────┐
     │              │
     ▼              ▼
Attendance      Activity
     │              │
     └──────┬───────┘
            ▼
       Participation
            │
            ▼
        Engagement
            │
            ▼
       Recognition


Study Session
     │
     ├── Participants
     ├── Attendance
     ├── Activities
     └── Analytics

# 11. Domain Entities

Domain entities represent concepts that possess identity within the platform.

An entity may change state over time while retaining its identity.

The principal domain entities are:

- Member
- Message
- AttendanceEvent
- ActivityEvent
- Session

---

## 11.1 Member

A Member represents an individual participating in the Bible study community.

The Member entity provides the identity against which participation and engagement are measured.

A Member may have:

- a unique identifier;
- a display name;
- participation history;
- attendance history;
- activity history;
- recognition history.

The Member entity should not contain presentation-specific information.

---

## 11.2 Message

A Message represents an individual communication extracted from a community conversation.

A Message may contain:

- sender identity;
- message content;
- timestamp;
- message type;
- source information.

Messages provide the raw conversational evidence from which higher-level domain events may be derived.

The Message entity should remain independent of the original export format.

---

## 11.3 AttendanceEvent

An AttendanceEvent represents a recognised attendance occurrence associated with a Member and a Session.

An AttendanceEvent may contain:

- member identity;
- session identity;
- attendance type;
- timestamp;
- supporting evidence.

Attendance events are derived from validated participation data according to the attendance rules defined by the platform.

---

## 11.4 ActivityEvent

An ActivityEvent represents a recognised activity performed by a Member.

Examples include:

- scripture reading;
- response;
- question;
- insight;
- prayer participation;
- other recognised activities.

An ActivityEvent may contain:

- member identity;
- activity type;
- session identity;
- timestamp;
- supporting message information.

Activity events provide the foundation for participation analytics.

---

## 11.5 Session

A Session represents a defined Bible study activity period.

A Session provides the analytical boundary within which attendance and participation are evaluated.

A Session may contain:

- session identity;
- date;
- topic;
- messages;
- attendance events;
- activity events;
- analytical results.

The Session entity provides the central context for session-level analysis.

---

# 12. Value Objects

Value objects represent descriptive domain concepts that are defined by their values rather than by independent identity.

Potential value objects include:

- MemberId
- SessionId
- MessageTimestamp
- ActivityType
- AttendanceType
- SessionDate
- ParticipationScore

Value objects should be:

- immutable where practical;
- validated at creation;
- free from unnecessary infrastructure dependencies.

---

## 12.1 ActivityType

ActivityType identifies the category of activity performed by a participant.

Examples may include:

- Scripture Reading
- Response
- Question
- Insight
- Prayer
- Other recognised activity categories

ActivityType provides a controlled vocabulary for activity classification.

---

## 12.2 AttendanceType

AttendanceType identifies the nature of an attendance occurrence.

The specific values are defined by the platform's participation and attendance rules.

The use of a defined type prevents inconsistent representation of attendance states.

---

## 12.3 ParticipationScore

ParticipationScore represents a calculated measure of participation.

A participation score should be treated as a domain value rather than an arbitrary user interface number.

The calculation of the score must follow the rules defined by the Participation Model and Analytics Engine.

---

# 13. Domain Services

Domain services contain domain operations that do not naturally belong to a single entity.

A domain service should be used when:

- the operation represents meaningful domain behaviour;
- multiple entities are involved;
- placing the behaviour on one entity would create an inappropriate responsibility.

Examples include:

- SessionDetectionService
- ParticipationAnalysisService
- AttendanceCalculationService
- ActivityClassificationService
- RecognitionService

Domain services must remain independent of presentation technologies and infrastructure implementations.

---

# 14. Domain Service Responsibilities

## Session Detection Service

Identifies and constructs study sessions from validated message data.

Responsibilities include:

- identifying session boundaries;
- grouping relevant messages;
- associating messages with sessions;
- producing session structures.

---

## Attendance Calculation Service

Determines attendance outcomes from validated participation evidence.

Responsibilities include:

- evaluating attendance criteria;
- associating attendance with sessions;
- calculating attendance summaries;
- supporting attendance trends.

---

## Activity Classification Service

Classifies recognised participant activities.

Responsibilities include:

- identifying activity types;
- applying classification rules;
- producing ActivityEvents;
- supporting activity aggregation.

---

## Participation Analysis Service

Analyses participation across sessions and time periods.

Responsibilities include:

- calculating participation measures;
- aggregating participant activity;
- identifying participation patterns;
- supporting engagement analysis.

---

## Recognition Service

Evaluates participation and attendance patterns against recognition rules.

Responsibilities include:

- evaluating achievement criteria;
- identifying qualifying participants;
- generating recognition results.

Recognition rules remain domain rules and should not be implemented in the Presentation Layer.

# 15. Aggregate Boundaries

Aggregates define consistency boundaries within the Domain Layer.

An aggregate groups related domain objects that should be treated as a single unit for specific domain operations.

The platform's principal aggregate boundaries are:

- Session Aggregate
- Member Participation Aggregate

---

## 15.1 Session Aggregate

The Session Aggregate represents a single Bible study session and its associated analytical activity.

```text
Session
   │
   ├── Messages
   │
   ├── Attendance Events
   │
   ├── Activity Events
   │
   └── Session Analytics
```

The Session serves as the primary aggregate root.

Operations involving the consistency of a session should be coordinated through the Session Aggregate.

The aggregate provides the context for:

- session participation;
- attendance;
- activity;
- session-level analytics.

---

## 15.2 Member Participation Aggregate

The Member Participation Aggregate represents a participant's activity across one or more sessions.

```text
Member
   │
   ├── Attendance History
   │
   ├── Activity History
   │
   ├── Participation Metrics
   │
   └── Recognition Results
```

This aggregate supports longitudinal analysis of individual participation.

It enables the platform to evaluate:

- attendance consistency;
- participation frequency;
- activity patterns;
- engagement trends;
- recognition eligibility.

---

# 16. Domain Relationships

The primary domain relationships are illustrated below.

```text
Member
   │
   │ participates in
   ▼
Session
   │
   ├───────────────┐
   ▼               ▼
Attendance      Activity
   │               │
   └───────┬───────┘
           ▼
     Participation
           │
           ▼
       Engagement
           │
           ▼
      Recognition
```

A Member may participate in multiple Sessions.

A Session may contain multiple Members.

A Member may produce multiple ActivityEvents within a Session.

Attendance and activity together provide evidence for participation analysis.

Participation patterns contribute to engagement analysis and recognition.

---

# 17. Domain Events

Domain events represent significant occurrences within the domain.

Potential domain events include:

- SessionDetected
- AttendanceRecorded
- ActivityRecorded
- ParticipationCalculated
- RecognitionAwarded

Domain events communicate that something meaningful has occurred without requiring direct coupling between all interested components.

---

## 17.1 SessionDetected

Raised when a valid Bible study session has been identified.

Potential consumers include:

- analytics workflows;
- reporting workflows;
- session summaries.

---

## 17.2 AttendanceRecorded

Raised when attendance has been recognised for a participant.

Potential consumers include:

- attendance analytics;
- participation analysis;
- recognition evaluation.

---

## 17.3 ActivityRecorded

Raised when a recognised participant activity has been identified.

Potential consumers include:

- activity analytics;
- participation analysis;
- reporting.

---

## 17.4 ParticipationCalculated

Raised when participation analysis has been completed.

Potential consumers include:

- engagement analytics;
- recognition services;
- reporting services.

---

## 17.5 RecognitionAwarded

Raised when a participant satisfies a recognition rule.

Potential consumers include:

- recognition reporting;
- dashboards;
- notification systems.

---

# 18. Analytical Domain Model

The platform's analytical model transforms raw evidence into progressively higher-level domain information.

```text
Raw Message
     │
     ▼
Classified Activity
     │
     ▼
Attendance / Participation Event
     │
     ▼
Session Analytics
     │
     ▼
Member Analytics
     │
     ▼
Community Analytics
```

This progression preserves traceability between analytical conclusions and the underlying evidence.

---

# 19. Domain Behaviour

The Domain Layer is responsible for determining the meaning of analytical data.

Examples of domain behaviour include:

- determining whether participation satisfies attendance criteria;
- classifying messages into recognised activities;
- aggregating participant activity;
- calculating analytical measures;
- evaluating recognition rules;
- identifying engagement patterns.

The Domain Layer should produce meaningful domain results rather than expose raw technical processing details.

---

# 20. Domain Invariants

Domain invariants represent conditions that should remain true within the domain.

Examples include:

- An AttendanceEvent must be associated with a valid participant.
- An AttendanceEvent must be associated with a valid session.
- An ActivityEvent must have a recognised ActivityType.
- A Session must have a valid session boundary.
- Analytical results must be derived from valid source data.
- Recognition results must be based on defined recognition rules.

Domain invariants protect the integrity of the analytical model.

# 21. Domain Independence

The Domain Layer shall remain independent of external technical concerns.

Domain logic shall not depend directly upon:

- Streamlit;
- Pandas;
- Plotly;
- OpenAI;
- Gemini;
- Ollama;
- WhatsApp export formats;
- file systems;
- databases;
- network services.

External systems may provide data to the Domain Layer through appropriate application and infrastructure boundaries.

This independence protects the core business knowledge of the platform from changes in technology.

---

# 22. Domain Interfaces

Where the Domain Layer requires interaction with external capabilities, those interactions should be defined through abstractions.

Examples include:

- data repositories;
- analytics providers;
- persistence interfaces;
- external service contracts.

The Domain Layer should depend upon abstractions rather than concrete technical implementations.

This supports:

- testability;
- portability;
- maintainability;
- dependency inversion.

---

# 23. Business Rule Ownership

Business rules belong within the Domain Layer.

Examples include:

- attendance criteria;
- participation definitions;
- activity classification rules;
- recognition rules;
- analytical calculation rules.

Business rules shall not be duplicated across:

- user interface components;
- application services;
- infrastructure adapters;
- report generators.

A single authoritative implementation should exist for each important domain rule.

---

# 24. Domain Testing Strategy

The Domain Layer should be tested independently from external technologies.

Testing should include:

## Unit Testing

Individual entities, value objects, and domain services should be tested in isolation.

---

## Rule Testing

Business rules should be tested against:

- valid inputs;
- invalid inputs;
- boundary conditions;
- exceptional cases.

---

## Analytical Testing

Analytical calculations should be verified against known expected results.

---

## Invariant Testing

Domain invariants should be tested to ensure that invalid domain states cannot be created or processed.

The Domain Layer should be capable of extensive testing without requiring:

- a user interface;
- a database;
- an external API;
- an internet connection.

---

# 25. Domain Evolution

The Domain Layer is expected to evolve as understanding of the platform improves.

Future domain capabilities may include:

- richer engagement models;
- advanced participation metrics;
- community health indicators;
- longitudinal growth analytics;
- predictive participation models;
- additional recognition systems;
- support for multiple communities;
- cross-community analytics.

Domain evolution should preserve existing concepts and business rules wherever practical.

Significant changes should be documented through the appropriate Engineering Decision Records or Architecture Decision Records.

---

# 26. Architectural Constraints

The following constraints govern the Domain Layer.

- Domain logic shall remain independent of presentation technologies.
- Domain logic shall remain independent of infrastructure implementations.
- Business rules shall have a single authoritative owner.
- Domain models shall use meaningful domain language.
- Domain operations shall be deterministic wherever practical.
- Domain entities shall not contain unnecessary technical concerns.
- Analytical results shall remain traceable to valid source data.
- Changes to domain behaviour shall be documented and tested.

These constraints protect the long-term integrity of the platform's core knowledge.

---

# 27. Architectural Governance

Changes to the Domain Layer should be reviewed carefully because domain changes may affect multiple areas of the platform.

A domain change may affect:

- application workflows;
- analytics;
- reporting;
- AI summaries;
- dashboards;
- recognition;
- specifications;
- business documentation.

Significant domain changes should therefore be evaluated for downstream impact before implementation.

Where appropriate, the change should be documented through an Engineering Decision Record or Architecture Decision Record.

---

# 28. Related Documents

## Architecture Library

- ARC-001 System Architecture
- ARC-002 Application Architecture
- ARC-004 AI Architecture
- ARC-005 Reporting Architecture
- ARC-006 Presentation Architecture
- ARC-007 Infrastructure Architecture
- ARC-008 Data Architecture

## Business Documentation

- BUS-003 Requirements
- BUS-004 Business Rules
- BUS-006 Analytics Definitions
- BUS-007 Recognition Rules

## Specifications

- SPEC-001 Session Detection
- SPEC-002 Participation Model
- SPEC-003 Activity Classification
- SPEC-004 Analytics Engine
- SPEC-005 Recognition Engine

## TechAndMe Playbook

- TMP-003 Engineering Principles
- TMP-006 Architecture Review Process
- TMP-007 Checkpoint Framework
- TMP-008 Engineering Reference System

---

# 29. Revision History

| Version | Date | Description | Author |
|----------|------|-------------|--------|
| 1.0 | July 2026 | Initial Domain Architecture | TechAndMe |

---

# 30. Closing Reflection

The Domain Layer represents the knowledge that gives the platform its meaning.

It defines what attendance means.

It defines what participation means.

It defines what activities mean.

It defines how engagement is understood.

It defines how recognition is determined.

These concepts should remain protected from unnecessary dependence on technology.

As the platform evolves, data sources may change, AI providers may change, interfaces may change, and deployment models may change.

The domain should remain the stable centre around which those technologies evolve.

A strong domain architecture therefore protects not only software structure, but also the knowledge and purpose represented by the software.

That is the foundation upon which the Online Bible Study Attendance and Participation Analytics Platform is built.

---

**Online Bible Study Attendance and Participation Analytics Platform**

**Architecture Library**

**Building Better Software.**

**Building Better Engineers.**

*"One step at a time. All the way."*

© TechAndMe