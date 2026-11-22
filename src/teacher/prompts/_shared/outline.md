<glossary>
{% for term in glossary %}- {{ term.name }}{% if term.symbol %} (the paper's {{ term.symbol }}){% endif %}: {{ term.meaning }}
{% endfor %}</glossary>

<outline>
{% for c in outline %}- {{ c.name }}{% if c.purpose %}: {{ c.purpose }}{% endif %}
{% endfor %}</outline>
