# Security History Notes

This repository previously tracked a local `ext_key` file. The public branch history was rewritten on 2026-05-30 to remove that file from all commits.

Use this rule for any public trading or API repository:

- If a committed value was ever a real credential, rotate or revoke it.
- If a generated data file includes private account information, remove it from public history before pushing.
- If a full history rewrite is needed again, coordinate it before pushing shared branches.
