# Security History Notes

This repository previously tracked a local `ext_key` file. The current working tree removes it and ignores future local key files, but Git history still records that a file named `ext_key` existed.

The known historical local content inspected during cleanup was:

```text
test1
test2
```

Even when historical content looks like a placeholder, use this rule for any public trading or API repository:

- If a committed value was ever a real credential, rotate or revoke it.
- If a generated data file included private account information, remove it from public history before pushing.
- If a full history rewrite is needed, coordinate it before pushing shared branches.

## Rewrite Option

If future inspection finds real secrets in history, use a history rewrite tool such as `git filter-repo` before pushing:

```bash
git filter-repo --path ext_key --invert-paths
```

Only rewrite public history when you understand the impact on existing clones and collaborators.

