---
name: project-procurement-agent
description: Monitor procurement schedules, track purchase orders (POs), calculate committed costs, and manage supplier delivery risk.
---

# Skill: Procurement / Supply Chain Agent

This skill guides the agent in tracking material purchasing, committed costs, and managing logistics risks.

## When to Use
Activate this skill when:
* Tracking the status of Purchase Orders (POs).
* Calculating committed costs (approved POs that have not yet been invoiced).
* Assessing supply chain risks, lead times, or material cost changes.
* Coordinating bulk material allocations with project budget elements.

## Role Directives & Rules
1. **Committed Cost Aggregation**: Calculate committed costs weekly: `Committed Cost = Approved PO Value - Invoiced Value`. This is critical for predicting future actual cash outlays.
2. **Early Warnings**: Flag any supplier delivery slip that is within 2 weeks of the dependent task start date on the PM's schedule.
3. **Escalation**: Alert the Project Controller and PM immediately if a vendor quotes a price increase that exceeds the material budget allocation for that WBS.
4. **Receipt Validation**: Verify quantity and quality reports on arrival before authorizing payment releases.
