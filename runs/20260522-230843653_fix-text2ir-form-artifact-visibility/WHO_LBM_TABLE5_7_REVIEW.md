# WHO LBM TABLE 5-7 REVIEW

## Result

The issue found around `cha8.i5`, `cha8.i5.si1`, and `cha8.i5.si2` is handled as a common `form_artifact` visibility problem.

## Kept As Visible Prose

- `cha8.i5` remains a normal `item`.
- The visible prose before the form is preserved.
- The following normal note remains visible as a normal `note` node:
  - `cha8.i5.si2.not1`

## Isolated As Reference Artifacts

| nid | handling |
|---|---|
| `cha8.i5.si1` | Converted to hidden `form_artifact`; summary text only. |
| `cha8.i5.si2` | Converted to hidden `form_artifact`; summary text only. |
| `cha8.i5.art1` | Created for the large Table 5-7 form block; summary text only in visible `text`, raw trace retained under non-default-rendered data. |

## Default Visibility

Default review and candidate export use the shared artifact visibility model. Nodes tagged `form_artifact`, `not_selectable`, `layout_artifact`, or `sanitized_layout_artifact` are hidden by default even when their `kind` is `preformatted`.

## Boundary Check

The small regression fixture verifies that a normal heading/prose after a form block is not swallowed into the artifact:

- visible prose before Table 5 is preserved
- form rows are hidden
- `Laboratory biosecurity` remains visible
- literal PUA is zero
- artifact text is under the hard length limit and contains no checkbox cluster

For the full WHO LBM output, the original `cha8.i5` area now has zero default-visible form leakage and zero candidate export leakage.

The full regenerated output confirms that `Table 6` and `Table 7` occur only in the non-default-rendered artifact payload, not in default-visible node text or candidate rows.
