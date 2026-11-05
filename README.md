# memrepo Development

## Purpose

This project tracks software development tasks for the memrepo repository.

GitHub Issues are the primary records for requirements, defects, and technical investigations. GitHub Projects is used to track task status and development progress.

## Task Types

- Feature: New requirements or capabilities.
- Bug: Defects and unexpected behavior.
- Investigation: Technical questions requiring evidence-based investigation.
- Chore: Engineering maintenance.
- Docs: Documentation changes.

## Status Definitions

| Status | Description |
|---|---|
| Backlog | Recorded but not yet being processed |
| Clarifying | Requirement details need clarification |
| Investigating | Facts and evidence are being collected |
| Designing | Solutions and technical decisions are being evaluated |
| Ready | Definition of Ready is satisfied and implementation is approved |
| In Progress | Approved implementation is underway |
| Verifying | Implementation is complete and verification is in progress |
| Accepted | User has accepted the result |
| Done | Delivery records are complete and the task is closed |
| Blocked | Progress is prevented by an unresolved issue |
| Rejected | User has explicitly decided not to proceed |

## Workflow Rules

1. Every development task should have an Issue.
2. Every Issue should be associated with this Project.
3. A task must satisfy Definition of Ready before implementation.
4. Implementation must remain within the approved scope.
5. Verification must be recorded before acceptance.
6. Only the user can approve important decisions and final acceptance.
7. Blocked tasks must document the blocking reason and recovery conditions.
8. Rejected tasks must document the decision and its rationale.
9. Closing an Issue does not independently establish user acceptance.

## Source of Truth

- Issue: Requirement, defect, investigation, and acceptance information.
- Project: Task status and progress.
- Pull Request: Code changes and review evidence.
- GitHub Actions: Automated verification results.

Avoid duplicating the same information across multiple fields or records.