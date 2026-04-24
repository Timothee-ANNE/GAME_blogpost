import markdown
import yaml
from pathlib import Path
import html as html_module # Added for escaping
import re

# --- Directives Logic (from md2blog.py) ---
DIRECTIVE_RE = re.compile(r'^::(figure|video)\{([^}]*)\}\s*$', re.MULTILINE)

def parse_attrs(s):
    return {m.group(1): m.group(2) for m in re.finditer(r'(\w+)="([^"]*)"', s)}

def inline_md(text):
    # Basic bold/link support for captions
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text

def render_item_html(kind, attrs):
    src = attrs.get('src', '')
    cap = attrs.get('caption', '')
    cap_html = f'\n  <div class="figure-caption">{inline_md(cap)}</div>' if cap else ''
    if kind == 'figure':
        media = f'  <img src="{html_module.escape(src)}" alt="figure" loading="lazy">'
    else:
        media = f'  <video autoplay loop muted playsinline src="{html_module.escape(src)}"></video>'
    return f'<figure class="post-figure">\n{media}{cap_html}\n</figure>'

def process_directives(text):
    def replacer(m):
        kind = m.group(1)
        attrs = parse_attrs(m.group(2))
        return render_item_html(kind, attrs)
    return DIRECTIVE_RE.sub(replacer, text)

def get_abstract_html(text):
    if not text:
        return ""
    # Wrap in the section class we just styled in CSS
    return f'''
    <section class="abstract-section">
        <h2>Abstract</h2>
        <p>{text}</p>
    </section>
    '''

def process_citations(text, meta):
    bib_data = meta.get('references', {})
    if not bib_data:
        return text, ""

    citations_found = []
    citation_map = {} 
    
    def replace_cite(m):
        raw_keys = m.group(1)
        keys = [k.strip() for k in raw_keys.split(',')]
        
        nums_list = []
        for key in keys:
            if key not in bib_data:
                # Instead of a string, we add a tuple with a placeholder to keep unpacking consistent
                nums_list.append((f"??{key}??", "Reference not found in frontmatter"))
                continue
            
            if key not in citation_map:
                citation_map[key] = len(citations_found) + 1
                citations_found.append(key)
            
            num = citation_map[key]
            full_ref = html_module.escape(bib_data[key])
            nums_list.append((num, full_ref))
        
        # Now every item in nums_list is a tuple (n, ref), so unpacking won't fail
        formatted_nums = ", ".join([
            f'<span class="cite-ref-num" data-tooltip="{ref}">{n}</span>' 
            for n, ref in nums_list
        ])
        
        return f'<span class="cite-ref-group">[{formatted_nums}]</span>'

    processed_text = re.sub(r'\[\^([^\]]+)\]', replace_cite, text)

    if not citations_found:
        return processed_text, ""

    bib_html = '<section class="references-section"><h2>References</h2><ol>'
    for key in citations_found:
        bib_html += f'<li>{bib_data[key]}</li>'
    bib_html += '</ol></section>'
    
    return processed_text, bib_html

def convert_md_to_blog(md_file, template_file, output_file):
    # Load raw file content
    raw_content = Path(md_file).read_text(encoding='utf-8')
    
    # 1. Split Frontmatter and Content
    if raw_content.startswith('---'):
        _, fm_text, md_text = raw_content.split('---', 2)
        meta = yaml.safe_load(fm_text)
    else:
        meta = {}
        md_text = raw_content
    # 2. Process custom ::figure and ::video directives
    # This must happen before Markdown conversion so standard MD inside captions still works
    md_text = process_directives(md_text)

    # 3. Process Citations and generate Bibliography HTML
    # This handles the [^key] order and prepares the {{REFERENCES}} block
    md_text, bib_html = process_citations(md_text, meta)

    # 4. Convert standard Markdown to HTML
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
    body_html = md.convert(md_text)

    # 5. Load Template
    template = Path(template_file).read_text(encoding='utf-8')

    # 6. Format Header Elements (Authors and Links)
    author_html = "".join([
        f'<div class="author"><strong>{a["name"]}</strong><span class="affil">{a.get("affiliation", "")}</span></div>' 
        for a in meta.get('authors', [])
    ])
    
    links_html = "".join([
        f'<a href="{l["url"]}" class="btn">{l["label"]}</a>' 
        for l in meta.get('links', [])
    ])

    # 7. Final Replacements
    replacements = {
        '{{TITLE}}': meta.get('title', 'Untitled'),
        '{{DATE}}': meta.get('date', ''),
        '{{ABSTRACT}}': get_abstract_html(meta.get('abstract', '')),
        '{{AUTHORS}}': author_html,
        '{{LINKS}}': links_html,
        '{{TEASER_ITEMS}}': meta.get('teaser_items', ''),
        '{{TEASER_CAPTION}}': meta.get('teaser_caption', ''),
        '{{CONTENT}}': body_html,
        '{{REFERENCES}}': bib_html, # Injected at the bottom of the page
    }

    for key, val in replacements.items():
        template = template.replace(key, str(val))

    # Save the output file
    Path(output_file).write_text(template, encoding='utf-8')
    print(f"✓ Blog post generated: {output_file}")
    
if __name__ == "__main__":
    convert_md_to_blog('post.md', 'template.html', 'index.html')