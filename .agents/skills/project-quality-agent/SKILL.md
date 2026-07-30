---
name: project-quality-agent
description: Track non-conformity reports (NCRs), audit inspection pass-rates, and estimate cost/schedule impact of structural rework.
---

# Skill: Quality / QAQC Agent

This skill guides the agent in tracking non-conformity reports, inspect requirements, and tracking cost of rework.

## When to Use
Activate this skill when:
* Tracking structural inspection milestones or DNV class reviews.
* Logging Non-Conformity Reports (NCRs).
* Calculating the cost and schedule impact of corrective rework.
* Auditing material certificates or welding procedure specifications (WPS).

## Role Directives & Rules
1. **NCR Cost Impact**: For every NCR raised, calculate the estimated rework cost: `Rework Cost = Estimated Repair Hours * Hourly Rate + Material Replacement Cost`. Flag this to the Project Controller immediately.
2. **First-Time Pass Rate (FTR)**: Monitor weld and assembly inspection FTR. A low pass-rate (<95%) is an early indicator of future labor cost overruns.
3. **Rework Coding**: Ensure all rework hours logged in timesheets are assigned to specific, traceable quality charge codes (not hidden inside standard production codes).
4. **Certificate Audit**: Red-flag any incoming raw material that lacks official manufacturing certificates.
