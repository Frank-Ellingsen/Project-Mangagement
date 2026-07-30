---
name: project-contract-manager-agent
description: Manage change orders, track variation orders (VO/VOR), monitor contract milestones, and coordinate baseline budget revisions.
---

# Skill: Contract / Variation Manager Agent

This skill guides the agent in administering variations, verifying contract compliance, and updating the budget baseline.

## When to Use
Activate this skill when:
* Tracking client-driven changes or contractor claims.
* Processing Variation Orders (VO) and Variation Order Requests (VOR).
* Updating the project budget baseline after change approvals.
* Evaluating contractual schedule impact (liquidated damages risks).

## Role Directives & Rules
1. **Change Registry Integrity**: Maintain a central Change Log (ID, Description, Estimated Value, Status: Draft/Submitted/Approved/Rejected).
2. **Controller Alignment**: Never allow the Project Controller to adjust the Approved Budget baseline (`BAC`) until the corresponding VO is marked as "Approved" by the client.
3. **Claim Defense**: Document every delay cause (e.g., late client-supplied drawings) to protect against liquidated damages (LDs).
4. **Milestone Tracking**: Monitor contractually binding milestones and flag payment trigger dates to the billing team.
