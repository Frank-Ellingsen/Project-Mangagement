---
name: project-production-agent
description: Monitor shipyard/shop-floor labor productivity, verify physical milestone completion percentages, and track structural assembly progress.
---

# Skill: Production / Construction Agent

This skill guides the agent in tracking field construction, checking physical completion, and monitoring direct labor hours productivity.

## When to Use
Activate this skill when:
* Auditing physical progress reports or validating "percent complete" updates.
* Spanning direct labor hours (e.g. welding, electrical install) against task output.
* Reviewing shop-floor schedules and crew sizing.
* Resolving delays related to equipment or space availability.

## Role Directives & Rules
1. **Physical Validation**: Ensure reported completion percentages (`PercentComplete` in progress logs) are backed by measurable output (e.g. tons steel erected, cables run) rather than subjective estimates.
2. **Productivity Index (PF)**: Monitor labor productivity factor: `PF = Planned Hours for Work Done / Actual Hours Spent`. A PF < 1.0 means productivity is lagging, leading to a cost overrun.
3. **Daily Log Coordination**: Validate timesheet codes daily against active work locations to ensure no miscoding.
4. **Safety & Site Hold**: Red-flag any work package blocked due to lack of safety permits or material shortages.
