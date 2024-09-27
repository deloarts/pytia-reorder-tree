# default files

Explains the config of all default files.

All default files can be copied, renamed and edited to fit your needs.

## 1 properties.default.json

This file contains all part properties, which are required for this app.

- **Location**: [/pytia_reorder_tree/resources/properties.default.json](../pytia_reorder_tree/resources/properties.default.json)
- **Rename to**: `properties.json`

### 1.1 file content

```json
{
    "project": "pytia.project",
    "product": "pytia.product",
    "creator": "pytia.creator",
    "modifier": "pytia.modifier",
    "group": "pytia.group",
    "filter": "pytia.manufacturer"
}
```

### 4.2 description

name | type | description
--- | --- | ---
`generic` | `str` | The name of the property, which stores the value of `generic`.
