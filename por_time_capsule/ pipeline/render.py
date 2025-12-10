import os
from jinja2 import Template

REPORT_TEMPLATE = """
<h1>PoR Time Capsule — Results</h1>
<p>Processed {{ n }} comments.</p>

<table border="1" cellpadding="6">
<tr>
<th>#</th>
<th>Comment</th>
<th>Stability</th>
<th>Coherence</th>
<th>Phase Lock</th>
<th>Total PoR</th>
</tr>

{% for i, r in enumerate(results) %}
<tr>
<td>{{ i+1 }}</td>
<td>{{ r.text }}</td>
<td>{{ "%.3f"|format(r.stability) }}</td>
<td>{{ "%.3f"|format(r.coherence) }}</td>
<td>{{ "%.3f"|format(r.phase_lock) }}</td>
<td><b>{{ "%.3f"|format(r.por_total) }}</b></td>
</tr>
{% endfor %}
</table>
"""

def render_html(results, save_path):
    tmpl = Template(REPORT_TEMPLATE)
    html = tmpl.render(results=results, n=len(results))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(html)

    return save_path

