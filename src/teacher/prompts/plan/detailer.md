# Component Detailer

You make one component of a method outline match the paper exactly. The outline was drafted from short notes, so its steps may be vague, incomplete, or filled in with what a standard method would do instead of what this paper does. You now have the full text of the sections that describe the component (`<source>`).

Rewrite the component's `purpose`, `inputs`, `steps` and `outputs` from `<source>`:
- Correct anything the source contradicts: which data a step uses, what is computed, in what order, what is kept and what is discarded.
- Add every step the source gives that the draft leaves out, and drop every step the source does not support.
- Keep the level of detail someone would need to implement it: each operation, what it acts on, and what it produces. Leave out values that are only tuning choices.
- Use the names in `<glossary>` for things it names, and refer to other components in `<outline>` by name instead of describing them again.

{% include "_shared/plain.md" %}

If the source does not describe the component at all, return the draft unchanged.
