# Canonical model.yml contract

Forge owns one reusable human-facing model-description contract for Forge
examples and CAD consumer repositories.

## Template

Use the exact template in `docs/templates/model.yml`.

The allowed fields are exactly:

- `section`: non-empty string;
- `priority`: positive integer;
- `title`: non-empty string;
- `tagline`: non-empty string;
- `description`: non-empty string;
- `parameters`: non-empty string;
- `stages`: non-empty list of non-empty strings.

Unknown fields are rejected. There is no consumer extension namespace inside
`model.yml`.

## Reuse

YAML parsing belongs to the caller. Reuse the executable Forge contract:

```python
import yaml
from scpf.model_metadata import validate_model_metadata

data = yaml.safe_load(path.read_text(encoding="utf-8"))
metadata = validate_model_metadata(data, label=str(path))
```

Do not copy the field list or type checks into a consumer repository.

## What does not belong here

`model.yml` is model/page description only. Do not put these categories in it:

- build participation, source paths or execution commands;
- source/build dependency graphs;
- verification expectations;
- generated command counts, status or current build facts;
- consumer-only presentation controls.

Those values belong in their owning CI, source, verification, generated-evidence
or separately named presentation source.
