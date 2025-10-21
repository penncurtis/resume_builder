from jinja2 import Environment, BaseLoader

def get_available_templates():
    return {
        "Modern Clean": "modern_clean",
        "Classic Serif": "classic_serif",
        "Compact Two-Column": "compact_two_col"
    }

# --- Jinja2 templates (kept inline for simplicity). Use semantic tags for fidelity. ---
TEMPLATES = {}

TEMPLATES["modern_clean"] = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  :root { --text:#1f2937; --muted:#6b7280; --accent:#111827; }
          body { margin:0; font-family: Inter, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; color: var(--text); font-size: 11px; background: #fff; }
          .page { padding: 36px 44px; background: #fff; }
          h1 { font-size: 26px; margin: 0 0 2px; font-weight: 700; letter-spacing: .2px; }
          .titleline { font-size: 11px; color: var(--muted); margin-bottom: 8px; }
          .contact { font-size: 11px; color: var(--muted); margin-bottom: 14px; }
          h2 { font-size: 11px; letter-spacing: .6px; text-transform: uppercase; color: var(--accent); margin: 18px 0 8px; border-bottom: 1px solid #e5e7eb; padding-bottom:4px;}
          .role { font-weight:600; font-size: 12px; }
          .meta { color: var(--muted); font-size: 11px; }l
  ul { margin: 6px 0 8px 18px; }
  li { margin: 2px 0; }
  .cols { display:grid; grid-template-columns: 2fr 1fr; gap: 24px; }
  small { color: var(--muted); }
</style>
</head>
<body>
<div class="page">
  <h1>{{ data.name or "Lorem Ipsum" }}</h1>
  <div class="titleline">{{ data.title or "Product Designer | UX Strategist | Creative Technologist" }}</div>
  <div class="contact">
    {{ (data.contact.get('email') if data.contact else None) or "lorem@ipsum.com" }}
    | {{ (data.contact.get('phone') if data.contact else None) or "555-555-5555" }}
    | {{ (data.contact.get('location') if data.contact else None) or "Lorem City, LC" }}
    {% if data.contact and data.contact.get('linkedin') %} | <strong>LinkedIn</strong> {{ data.contact.get('linkedin') }}{% endif %}
    {% if data.contact and data.contact.get('github') %} | <strong>GitHub</strong> {{ data.contact.get('github') }}{% endif %}
  </div>

  {% if data.summary %}
  <h2>Summary</h2>
  <p>{{ data.summary }}</p>
  {% endif %}

  <div class="cols">
    <section>
      <h2>Work Experience</h2>
      {% if data.experience %}
        {% for x in data.experience %}
          <div class="job">
            <div class="role">
              {{ x.get('title','Job Title') }} — {{ x.get('company','Company') }}
              {% if x.get('location') %}<span class="meta">| {{ x.get('location') }}</span>{% endif %}
            </div>
            <div class="meta">{{ x.get('start_date','Mon YYYY') }} – {{ x.get('end_date','Present') }}</div>
            {% if x.get('bullets') %}
              <ul>
                {% for b in x.get('bullets') %}<li>{{ b }}</li>{% endfor %}
              </ul>
            {% endif %}
            {% if x.get('technologies') %}
              <small><strong>Tech:</strong> {{ x.get('technologies')|join(", ") }}</small>
            {% endif %}
          </div>
        {% endfor %}
      {% else %}
        <p><em>Lorem ipsum placeholder experience with crisp bullets and dates.</em></p>
      {% endif %}
    </section>

    <aside>
      <h2>Education</h2>
      {% if data.education %}
        {% for e in data.education %}
          <div class="edu">
            <div class="role">{{ e.get('degree','Degree') }} — {{ e.get('school','University') }}</div>
            <div class="meta">
              {{ e.get('location','') }}{% if e.get('location') %} | {% endif %}
              {{ e.get('start_date','Mon YYYY') }} – {{ e.get('end_date','Mon YYYY') }}
            </div>
            {% if e.get('details') %}
              <ul>{% for d in e.get('details') %}<li>{{ d }}</li>{% endfor %}</ul>
            {% endif %}
          </div>
        {% endfor %}
      {% else %}
        <p><em>Lorem ipsum education block.</em></p>
      {% endif %}

      <h2>Skills</h2>
      {% set skills = data.skills or {} %}
      <ul>
        {% for k, v in skills.items() if v %}
          <li><strong>{{ k.replace("_"," ").title() }}:</strong> {{ v|join(", ") }}</li>
        {% endfor %}
        {% if not skills or not (skills.get('design') or skills.get('frontend') or skills.get('backend') or skills.get('data_ai') or skills.get('tools') or skills.get('other')) %}
          <li><strong>Design:</strong> Wireframing, Prototyping</li>
          <li><strong>Frontend:</strong> React, SwiftUI</li>
          <li><strong>Backend:</strong> Python, Flask</li>
        {% endif %}
      </ul>
    </aside>
  </div>
</div>
</body>
</html>
"""

TEMPLATES["classic_serif"] = r"""
<!doctype html>
<html><head><meta charset="utf-8">
        <style>
          body { margin:0; font-family: "Georgia", "Times New Roman", serif; color:#222; font-size: 11px; }
          .page { padding: 42px 50px; }
          h1 { margin:0 0 4px; font-size:28px; font-weight:700; letter-spacing:.2px; }
          .rule { height:1px; background:#000; margin:8px 0 12px; }
          .muted { color:#555; font-size:11px; }
          h2 { font-size:12px; margin: 14px 0 6px; text-transform:uppercase; letter-spacing:.6px; }
          li { margin: 3px 0; }
</style></head>
<body><div class="page">
  <h1>{{ data.name or "J. McJobface" }}</h1>
  <div class="muted">{{ data.contact.email or "hey@sheetstresumee.com" }} | {{ data.contact.phone or "(555) 555-5555" }} | {{ data.contact.location or "Denver, CO" }}</div>
  <div class="rule"></div>
  <div class="muted">{{ data.title or "Product Designer | UX Strategist | Creative Technologist" }}</div>

  {% if data.summary %}<h2>Professional Summary</h2><p>{{ data.summary }}</p>{% endif %}

  <h2>Work Experience</h2>
  {% for x in data.experience %}
    <p><strong>{{ x.title }}</strong>, {{ x.company }} <span class="muted">— {{ x.start_date }} – {{ x.end_date }}</span></p>
    {% if x.bullets %}<ul>{% for b in x.bullets %}<li>{{ b }}</li>{% endfor %}</ul>{% endif %}
  {% endfor %}
  {% if not data.experience %}<p><em>Experience placeholder…</em></p>{% endif %}

  <h2>Education</h2>
  {% for e in data.education %}
    <p><strong>{{ e.degree }}</strong>, {{ e.school }} <span class="muted">— {{ e.start_date }} – {{ e.end_date }}</span></p>
  {% endfor %}
  {% if not data.education %}<p><em>Education placeholder…</em></p>{% endif %}

  <h2>Certifications, Skills & Interests</h2>
  <ul>
    {% for k, v in data.skills.items() if v %}<li><strong>{{ k.replace("_"," ").title() }}:</strong> {{ v|join(", ") }}</li>{% endfor %}
    {% if not (data.skills.design or data.skills.frontend or data.skills.backend or data.skills.data_ai or data.skills.tools or data.skills.other) %}
      <li><strong>Skills:</strong> Lorem ipsum dolor sit amet…</li>
    {% endif %}
  </ul>
</div></body></html>
"""

TEMPLATES["compact_two_col"] = r"""
<!doctype html>
<html><head><meta charset="utf-8">
        <style>
          body { margin:0; font-family: "Inter", system-ui, -apple-system; color:#222; font-size: 11px; }
          .page { padding: 28px 32px; }
          .grid { display:grid; grid-template-columns: 1fr 1fr; gap: 18px; }
          h1 { margin:0; font-size:24px; font-weight:800; }
          .muted { color:#666; font-size:11px; margin-bottom:6px; }
          h2 { font-size:11px; margin: 12px 0 6px; text-transform:uppercase; letter-spacing:.6px; }
          ul { margin:6px 0 8px 18px; }
</style></head>
<body><div class="page">
  <h1>{{ data.name or "Lorem Ipsum" }}</h1>
  <div class="muted">{{ data.title or "Creative Technologist" }} • {{ data.contact.email or "lorem@ipsum.com" }} • {{ data.contact.phone or "555-555-5555" }}</div>
  <div class="grid">
    <section>
      <h2>Experience</h2>
      {% for x in data.experience %}
        <p><strong>{{ x.title }}</strong> — {{ x.company }}<br><span class="muted">{{ x.start_date }} – {{ x.end_date }}{% if x.location %} • {{ x.location }}{% endif %}</span></p>
        {% if x.bullets %}<ul>{% for b in x.bullets %}<li>{{ b }}</li>{% endfor %}</ul>{% endif %}
      {% endfor %}
      {% if not data.experience %}<p><em>Experience placeholder…</em></p>{% endif %}
    </section>
    <aside>
      {% if data.summary %}<h2>Summary</h2><p>{{ data.summary }}</p>{% endif %}
      <h2>Education</h2>
      {% for e in data.education %}
        <p><strong>{{ e.degree }}</strong>, {{ e.school }}<br><span class="muted">{{ e.start_date }} – {{ e.end_date }}</span></p>
      {% endfor %}
      {% if not data.education %}<p><em>Education placeholder…</em></p>{% endif %}

      <h2>Skills</h2>
      <ul>
        {% for k, v in data.skills.items() if v %}
          <li><strong>{{ k.replace("_"," ").title() }}:</strong> {{ v|join(", ") }}</li>
        {% endfor %}
      </ul>
    </aside>
  </div>
</div></body></html>
"""

def render_template_html(data: dict, template_name: str) -> str:
    key = get_available_templates()[template_name]
    env = Environment(loader=BaseLoader(), autoescape=True)
    tmpl = env.from_string(TEMPLATES[key])
    return tmpl.render(data=data)