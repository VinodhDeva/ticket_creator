# Jira Cloud steps

Use the connected Atlassian MCP tools for every call below. Use the `site` from the team config as the cloud site. If the Atlassian tools are not available, stop and tell the user to authorize the connector through `/mcp`.

## Step 1: Fetch the parent and any existing children

1. Get the parent issue with `summary`, `description`, `issuetype`, `status`, `comment`, and `parent`.
2. Search for existing children with this JQL, and keep their summaries:

   ```
   parent = PARENT-KEY
   ```

## Before the preview: Resolve the child type

Read `issuetype.hierarchyLevel` from the parent.

| Parent level | Example | Child type |
|---|---|---|
| `1` or higher | Epic | `child_issue_type` |
| `0` | Story, Task, Bug | `subtask_issue_type` |
| `-1` | Sub-task | None. Stop, because a sub-task cannot have children |

When the child type is `subtask_issue_type`, add this warning to the preview: "Sub-task points usually do not count toward sprint velocity."

Then get the create metadata for the parent's project and the resolved child type. Confirm that `points_field` is in the returned fields. If it is missing, stop before creating anything, and show the user the returned fields whose names contain "point" or "estimate". Team-managed and company-managed projects often use different field IDs.

## Step 6: Create approved children

Create children in the parent's project, in dependency order. Skip any child whose summary matches an existing child from step 1. Set these fields on each new issue:

| Field | Value |
|---|---|
| `project` | The parent's project key |
| `issuetype` | The child type resolved above |
| `summary` | Child title |
| `description` | Child ticket body, in the format the tool accepts |
| `parent` | The parent's key |
| `points_field` value | Points as a number, not a string |

In the child ticket body, use Jira keys in `Parent:` and `Depends on`. Do not add `points:` labels.

Read the first created issue back, and confirm that its parent and points field are set. If either is wrong, stop and report before creating more. If any call fails, stop and report which children were created.
