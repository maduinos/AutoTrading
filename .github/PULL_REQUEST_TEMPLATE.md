## Summary

- 

## Scope

- [ ] Documentation only
- [ ] Import-safe helper change
- [ ] Credential/data safety change
- [ ] Test or CI change

## Checks

- [ ] Ran `python3 -m unittest discover -s tests -v`
- [ ] Ran `python3 -m py_compile autotrading.py data_history.py get_mass_data.py tests/test_autotrading.py tests/test_data_history.py tests/test_get_mass_data.py`
- [ ] Did not add `ext_key`, `.env`, logs, generated data, or real account details
- [ ] Did not add financial advice or live-order behavior without explicit safety notes

