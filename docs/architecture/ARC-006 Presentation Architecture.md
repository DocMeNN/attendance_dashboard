# Online Bible Study Attendance and Participation Analytics Platform

# ARC-006

# Presentation Architecture

---

## Document Information

| Property | Value |
|----------|-------|
| Document ID | ARC-006 |
| Title | Presentation Architecture |
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
4. Role of the Presentation Layer
5. Presentation Principles
6. Presentation Architecture Overview
7. Streamlit Application Framework
8. Application Navigation
9. Related Documents
10. Revision History
11. Closing Reflection

---

# Preamble

The Presentation Layer provides the human interface to the Online Bible Study Attendance and Participation Analytics Platform.

It allows users to:

- import data;
- view analytical results;
- explore attendance;
- examine activity;
- review participation;
- view reports;
- interact with AI-assisted capabilities;
- configure application settings.

The Presentation Layer is responsible for communicating with users.

It is not responsible for owning the core business rules of the platform.

The architecture therefore separates:

```text
User Interface
      │
      ▼
Presentation Logic
      │
      ▼
Application Services
      │
      ▼
Domain and Analytics
```

This separation allows the user interface to evolve without requiring changes to the core analytical model.

---

# 1. Purpose

The purpose of this document is to define the architecture of the Presentation Layer.

It establishes:

- presentation responsibilities;
- page architecture;
- navigation;
- ViewModels;
- presentation components;
- user interaction patterns;
- AI presentation integration;
- error and loading states.

This document serves as the authoritative architectural reference for the platform's user-facing layer.

---

# 2. Scope

This document covers the Presentation Layer.

It includes:

- Streamlit application structure;
- page architecture;
- navigation;
- ViewModels;
- presentation components;
- user interaction;
- dashboard presentation;
- AI presentation components.

It does not define:

- domain rules;
- analytical algorithms;
- AI provider implementations;
- data storage;
- deployment infrastructure.

Those concerns are documented separately.

---

# 3. Role of the Presentation Layer

The Presentation Layer translates application capabilities into user-facing interactions.

Its responsibilities include:

- displaying information;
- receiving user input;
- initiating application actions;
- displaying application results;
- displaying loading states;
- displaying errors;
- providing navigation.

The Presentation Layer should not independently determine the meaning of domain data.

---

# 4. Presentation Principles

The Presentation Architecture follows the following principles.

## Separation of Concerns

Presentation code should remain separate from business logic.

---

## Application Delegation

User actions should be delegated to Application Layer services.

---

## Consistent User Experience

Similar actions should produce consistent interface behaviour.

---

## Explicit State Handling

Loading, success, empty, and error states should be handled explicitly.

---

## Component Reuse

Common interface elements should be implemented as reusable components.

---

## Accessibility and Clarity

Information should be presented in a clear and understandable manner.

---

## Responsive Design

The interface should support practical use across different screen sizes where the framework permits.

---

# 5. Presentation Architecture Overview

The high-level Presentation Architecture is:

```text
User
 │
 ▼
Presentation Layer
 │
 ├── Navigation
 ├── Pages
 ├── Components
 └── ViewModels
        │
        ▼
Application Layer
        │
        ▼
Domain Layer
        │
        ▼
Infrastructure Layer
```

The Presentation Layer provides the entry point for user interaction.

It delegates application work to the Application Layer.

---

# 6. Streamlit Application Framework

The platform uses Streamlit as its primary presentation framework.

Streamlit provides:

- rapid interface development;
- interactive data visualisation;
- Python-native integration;
- dashboard capabilities;
- analytical exploration.

The platform's architecture should avoid allowing framework-specific concerns to spread throughout the entire application.

Streamlit-specific implementation should remain primarily within the Presentation Layer.

---

# 7. Application Navigation

The application provides navigation between major functional areas.

The primary navigation structure includes:

```text
Application
    │
    ├── Home
    ├── Dashboard
    ├── Attendance
    ├── Activity
    ├── Reports
    └── Settings
```

Navigation should provide users with clear access to the major capabilities of the platform.

Navigation logic should remain separate from domain and analytical logic.

---

# 8. Related Documents

## Architecture Library

- ARC-001 System Architecture
- ARC-002 Application Architecture
- ARC-003 Domain Architecture
- ARC-004 AI Architecture
- ARC-005 Reporting Architecture
- ARC-007 Infrastructure Architecture
- ARC-008 Data Architecture

## Business Documentation

- BUS-003 Requirements
- BUS-006 Analytics Definitions
- BUS-008 Reporting Definitions

## Specifications

- SPEC-004 Analytics Engine
- SPEC-006 AI Summary Engine
- SPEC-007 Reporting Specification

## TechAndMe Playbook

- TMP-003 Engineering Principles
- TMP-006 Architecture Review Process
- TMP-008 Engineering Reference System

# 8. Page Architecture

Each major application capability is represented by a dedicated presentation page.

A page is responsible for:

- presenting a specific functional area;
- collecting user input;
- invoking appropriate application services;
- displaying results;
- handling presentation state.

The current page structure includes:

```text
Pages
 │
 ├── Home
 ├── Dashboard
 ├── Attendance
 ├── Activity
 ├── Reports
 └── Settings
```

Pages should remain focused on presentation concerns.

They should not contain:

- domain rules;
- analytical algorithms;
- provider-specific AI logic;
- infrastructure implementation details.

---

# 9. ViewModel Architecture

ViewModels provide a presentation-oriented interface between pages and application services.

The general flow is:

```text
Page
 │
 ▼
ViewModel
 │
 ▼
Application Service
 │
 ▼
Domain / Analytics
```

A ViewModel may be responsible for:

- preparing data for presentation;
- coordinating user actions;
- invoking application services;
- managing presentation state;
- transforming application results into UI-ready structures.

ViewModels should not become a second Domain Layer.

They should coordinate presentation behaviour rather than own core business rules.

---

# 10. Presentation Components

Reusable interface elements should be implemented as presentation components.

Examples include:

- buttons;
- cards;
- tables;
- charts;
- status indicators;
- loading indicators;
- error displays;
- AI panels.

Components should be designed for reuse where the same presentation behaviour occurs in multiple locations.

---

# 11. Dashboard Presentation

The Dashboard provides a consolidated view of important analytical information.

It may display:

- attendance metrics;
- participation metrics;
- activity metrics;
- recognition information;
- trends;
- AI-assisted insights.

The Dashboard should consume analytical results prepared by the Application and Reporting Layers.

It should not independently calculate authoritative metrics.

---

# 12. Attendance Page

The Attendance Page provides access to attendance-related analytical information.

Potential presentation elements include:

- attendance summaries;
- attendance trends;
- member attendance records;
- attendance comparisons.

The page should delegate attendance calculations to the appropriate application services.

---

# 13. Activity Page

The Activity Page presents participant activity information.

Potential presentation elements include:

- activity summaries;
- activity distributions;
- activity trends;
- activity rankings.

Activity classification and analytical calculations remain outside the Presentation Layer.

---

# 14. Reports Page

The Reports Page provides access to generated analytical reports.

Potential capabilities include:

- selecting report types;
- viewing reports;
- generating reports;
- exporting reports;
- requesting AI-assisted summaries.

The page should delegate report generation to the Reporting Layer.

---

# 15. Settings Page

The Settings Page provides configuration controls for the application.

Potential settings include:

- AI provider selection;
- application preferences;
- display preferences;
- configuration status.

Settings should be validated and processed through appropriate application or infrastructure boundaries.

---

# 16. AI Presentation Architecture

AI capabilities are exposed to users through dedicated presentation components.

The AI presentation architecture is:

```text
AI Page / Panel
      │
      ▼
AI ViewModel
      │
      ▼
AI Application Service
      │
      ▼
AI Task
      │
      ▼
AI Provider
```

AI presentation components may include:

- AI action buttons;
- provider selectors;
- provider status indicators;
- loading indicators;
- error displays;
- result displays;
- summary cards.

The Presentation Layer should not contain:

- provider-specific SDK calls;
- prompt construction;
- AI provider selection logic;
- AI business rules.

---

# 17. User Interaction Flow

The general user interaction flow is:

```text
User Action
     │
     ▼
Presentation Component
     │
     ▼
ViewModel
     │
     ▼
Application Service
     │
     ▼
Domain / Analytics / AI
     │
     ▼
Application Result
     │
     ▼
ViewModel
     │
     ▼
Presentation Component
```

This flow ensures that user interface components remain focused on interaction and presentation.

---

# 18. Presentation State

The Presentation Layer should explicitly manage relevant interface states.

Common states include:

```text
Initial
  │
  ▼
Loading
  │
  ├──────────────┐
  ▼              ▼
Success        Error
  │
  ▼
Displayed
```

Additional states may include:

- empty;
- unavailable;
- partially loaded;
- cancelled.

Explicit state handling improves user understanding and application reliability.

---

# 19. Loading States

Long-running operations should provide visible feedback.

Examples include:

- data import;
- analytical processing;
- report generation;
- AI generation.

The user should be informed when an operation is:

- starting;
- in progress;
- complete;
- unsuccessful.

The interface should avoid leaving the user uncertain about whether an action has been processed.

---

# 20. Error Presentation

Errors should be presented in a manner appropriate to the user.

The Presentation Layer should:

- display understandable error messages;
- avoid exposing unnecessary technical details;
- preserve useful diagnostic information where appropriate;
- provide recovery guidance when possible.

The Presentation Layer should not independently determine the underlying cause of application errors.

Errors should be translated into user-facing messages at the appropriate boundary.

---

# 21. Presentation Data Transformation

Application and domain models may not be directly suitable for display.

The Presentation Layer may transform application results into presentation-specific structures.

```text
Domain / Application Result
          │
          ▼
   Presentation Mapping
          │
          ▼
       View Model
          │
          ▼
       UI Display
```

Presentation transformation may include:

- formatting dates;
- formatting numbers;
- preparing chart data;
- preparing table rows;
- preparing display labels.

Such transformations should not alter the underlying domain meaning.

---

# 22. Session State

The application may maintain presentation state required for the current user interaction.

Examples include:

- selected page;
- imported dataset;
- selected session;
- selected member;
- selected AI provider;
- generated AI result.

Session state should be managed deliberately.

It should not become an uncontrolled substitute for domain persistence or application state management.

---

# 23. Navigation State

Navigation state determines which functional area is currently displayed.

The navigation architecture should provide:

- predictable page transitions;
- clear current-page identification;
- consistent navigation behaviour.

Navigation state should remain separate from domain state.

A change in the selected page should not alter domain data unless an explicit user action invokes an application operation.

---

# 24. Presentation Testing Strategy

The Presentation Layer should be tested at multiple levels.

## Component Testing

Reusable presentation components should be tested for:

- correct rendering;
- expected interaction;
- valid state handling;
- error presentation.

---

## ViewModel Testing

ViewModels should be tested for:

- correct application service invocation;
- correct state transitions;
- correct presentation data transformation;
- appropriate error handling.

---

## Page Testing

Pages should be tested for:

- correct user workflows;
- correct navigation;
- correct data display;
- correct handling of empty and error states.

---

# 25. Accessibility and Usability

The Presentation Layer should aim to make analytical information understandable and usable.

The interface should consider:

- clear labels;
- readable information;
- understandable error messages;
- consistent navigation;
- appropriate visual hierarchy;
- meaningful chart descriptions where practical.

The presentation of analytical results should not depend solely on visual elements where textual interpretation is necessary.

---

# 26. Presentation Performance

Presentation performance should be considered as data volume and analytical complexity increase.

Potential strategies include:

- avoiding unnecessary recalculation;
- reusing prepared analytical results;
- limiting unnecessary rerendering;
- using appropriate data loading strategies;
- displaying progress for long-running operations.

Performance optimisation should not compromise the correctness of displayed results.

---

# 27. Presentation Extensibility

The Presentation Architecture should support the addition of new pages and components without destabilising existing functionality.

Future presentation capabilities may include:

- additional analytical pages;
- mobile-optimised interfaces;
- advanced filtering;
- interactive exploration;
- additional dashboards;
- custom report views;
- conversational AI interfaces.

New presentation capabilities should continue to respect the boundary between:

```text
Presentation
      │
      ▼
Application
      │
      ▼
Domain
```

---

# 28. Architectural Constraints

The following constraints govern the Presentation Layer.

- Presentation code shall not own core business rules.
- Pages shall delegate application operations to appropriate services.
- UI components shall not directly access infrastructure implementations.
- Provider-specific AI logic shall remain outside the Presentation Layer.
- ViewModels shall not become a replacement for the Domain Layer.
- Navigation state shall remain separate from domain state.
- Loading, success, empty, and error states should be handled explicitly.
- Presentation transformations shall not alter domain meaning.

These constraints preserve the separation between user interaction and application knowledge.

---

# 29. Architectural Governance

Significant changes to presentation architecture should be reviewed before implementation.

Examples include:

- changing the presentation framework;
- changing the navigation model;
- introducing a new state-management approach;
- introducing a mobile-specific presentation layer;
- changing the ViewModel architecture;
- introducing a new user interaction paradigm.

Significant changes should be documented through the appropriate Engineering Decision Record or Architecture Decision Record.

---

# 30. Related Documents

## Architecture Library

- ARC-001 System Architecture
- ARC-002 Application Architecture
- ARC-003 Domain Architecture
- ARC-004 AI Architecture
- ARC-005 Reporting Architecture
- ARC-007 Infrastructure Architecture
- ARC-008 Data Architecture
- ARC-009 Security Architecture

## Business Documentation

- BUS-003 Requirements
- BUS-006 Analytics Definitions
- BUS-008 Reporting Definitions

## Specifications

- SPEC-004 Analytics Engine
- SPEC-006 AI Summary Engine
- SPEC-007 Reporting Specification

## TechAndMe Playbook

- TMP-003 Engineering Principles
- TMP-006 Architecture Review Process
- TMP-007 Checkpoint Framework
- TMP-008 Engineering Reference System
- TMP-127 AI-Assisted Software Engineering Framework

---

# 31. Revision History

| Version | Date | Description | Author |
|----------|------|-------------|--------|
| 1.0 | July 2026 | Initial Presentation Architecture | TechAndMe |

---

# 32. Closing Reflection

The Presentation Layer is the point at which the platform becomes accessible to its users.

Behind the interface are domain models, analytical engines, reporting services, data pipelines, and AI capabilities.

The Presentation Layer brings these capabilities together in a form that people can understand and use.

However, the interface should not become the owner of the knowledge it displays.

Its role is to:

- receive interaction;
- communicate intent;
- present information;
- provide feedback.

The underlying application and domain architecture remain responsible for the meaning of the information.

This separation allows the platform to evolve.

The interface may change.

The presentation framework may change.

The interaction model may change.

Yet the core analytical and domain knowledge can remain stable.

That is the purpose of the Presentation Architecture.

---

**Online Bible Study Attendance and Participation Analytics Platform**

**Architecture Library**

**Building Better Software.**

**Building Better Engineers.**

*"One step at a time. All the way."*

© TechAndMe