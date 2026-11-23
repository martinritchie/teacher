<heard>
{{ heard }}
</heard>

<introduction>
{{ introduction }}
</introduction>

<conclusion>
{{ conclusion }}
</conclusion>
{% if problems %}
<draft>
{{ draft.spoken() | join("\n\n") }}
</draft>
{% endif %}{% include "_shared/problems.md" %}
Write the contributions part.
