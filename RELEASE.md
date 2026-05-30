# Release Process

This is a personal lab repository. Releases are optional and should be used only when a stable public snapshot is useful.

## Before Release

1. Run `python3 -m py_compile autotrading.py data_history.py get_mass_data.py`.
2. Update `CHANGELOG.md`.
3. Confirm no local secrets, account data, generated data, or logs are tracked.
4. Confirm README still clearly says this is not financial advice.

## Secret-History Reminder

If a real credential was ever committed, delete or rotate the credential before publishing a release. Removing a file from the latest commit does not remove it from Git history.
