# split-ticket

A [Claude Code](https://claude.com/claude-code) skill that splits a large tracker ticket into independently deliverable child tickets and sizes each one in story points, using your team's days-per-point rate.

Nothing is written to your tracker until you approve a preview.

## What it does

1. Reads the parent ticket and any children it already has.
2. Drafts child tickets that can each ship on their own, and maps every parent acceptance criterion to a child.
3. Estimates days for each child and converts days to points with a script, so the same days always give the same points.
4. Sends any child larger than `max_points` back to be split again.
5. Shows a preview with totals, uncovered criteria, and open questions, then waits for your approval.
6. Creates the approved children in dependency order and links them to the parent. Reruns skip children that already exist.

## Tracker support

| Tracker | Status | Points stored as | Children linked with |
|---|---|---|---|
| GitHub Issues | Tested end to end | `points:N` label | Sub-issues |
| Jira Cloud | Written, not yet run against a live Jira site | Custom field set by `points_field` | `parent` field |
| Linear, Asana, ClickUp, Monday | No dedicated steps. Claude uses the connected MCP tools | Depends on the tracker | Depends on the tracker |

Jira Data Center is not supported.

## Requirements

- Claude Code
- Python 3 (standard library only)
- For GitHub: [`gh`](https://cli.github.com/), logged in with `gh auth login`
- For Jira and other trackers: that tracker's MCP connector, authorized through `/mcp`

## Install

Clone this repository and open Claude Code in it:

```bash
git clone https://github.com/VinodhDeva/ticket_creator.git
```

To use the skill in another project, copy `.claude/skills/split-ticket` into that project's `.claude/skills/` folder. The skill's commands use paths relative to the project root.

## Usage

```text
/split-ticket https://github.com/OWNER/REPO/issues/1
/split-ticket PAY-123 for team payments
```

The skill uses `teams/default.json` when you name no team.

## Team configuration

Each team has one JSON file in `.claude/skills/split-ticket/teams/`.

```json
{
  "team": "default",
  "tracker": "github",
  "days_per_point": 1.5,
  "scale": [1, 2, 3, 5, 8],
  "max_points": 5,
  "points_label_prefix": "points:"
}
```

| Field | Meaning |
|---|---|
| `team` | Team name |
| `tracker` | `github`, `jira`, or another connected tracker |
| `days_per_point` | Working days that one point represents |
| `scale` | Allowed point values |
| `max_points` | Largest allowed child. Anything larger must be split |
| `points_label_prefix` | Label prefix for trackers with no points field |

### How points are calculated

`points = days / days_per_point`, rounded up to the next value in `scale`.

With `days_per_point` set to 1.5 and the scale above, 3 days is 2 points, 4 days is 3 points, and 5 days is 5 points. Because points round up, the total capacity in days can be higher than the total estimated days.

### Jira setup

1. Authorize the Atlassian connector through `/mcp`.
2. Copy `teams/jira.example.json` to `teams/<team>.json`.
3. Set these fields, along with `days_per_point`, `scale`, and `max_points`:

| Field | Meaning |
|---|---|
| `site` | Your Atlassian site, such as `your-company.atlassian.net` |
| `points_field` | Custom field ID that stores points. It varies by site and can vary by project |
| `child_issue_type` | Issue type for children of an Epic |
| `subtask_issue_type` | Issue type for children of a Story, Task, or Bug |

Children are created in the parent's project. If `points_field` is not available for the project and issue type, the run stops before creating anything and lists likely fields.

Split Epics where possible. When the parent is a Story, Task, or Bug, children must be sub-tasks, and sub-task points usually do not count toward sprint velocity.

## Tests

```bash
python3 .claude/skills/split-ticket/scripts/test_points.py
```

## Project layout

```text
.claude/skills/split-ticket/
├── SKILL.md                 Workflow Claude follows
├── references/jira.md       Jira-specific steps
├── scripts/points.py        Days-to-points conversion
├── scripts/test_points.py   Script tests
└── teams/                   One configuration file per team
```
