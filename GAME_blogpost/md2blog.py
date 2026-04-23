#!/usr/bin/env python3
"""
md2blog.py — Convert a Markdown blog post to a polished HTML page.

Usage:
    python md2blog.py post.md                     # writes post.html next to post.md
    python md2blog.py post.md -o output.html      # custom output path
    python md2blog.py post.md -t my_template.html # custom template

Markdown extensions supported:
  - Standard markdown (headers, bold, italic, lists, blockquotes, links, images)
  - Fenced code blocks
  - Footnotes
  - LaTeX math: inline $...$ and display $$...$$
  - Custom figure directive:
      ::figure{src="path/to/image.png" caption="Caption text here"}
  - Custom video directive:
      ::video{src="path/to/video.mp4" caption="Caption text here"}

Front matter (YAML between --- delimiters) supports:
    title, date, authors (list of {name, affiliation}), abstract,
    links (list of {label, url})
"""

import argparse, os, re, sys, html as html_module
from pathlib import Path
import markdown

# ── YAML front-matter parser ──────────────────────────────────────────────────

def parse_frontmatter(text):
    meta = {}
    if not text.startswith('---'):
        return meta, text
    end = text.find('\n---', 3)
    if end == -1:
        return meta, text
    fm_text = text[3:end].strip()
    body = text[end + 4:].lstrip('\n')

    current_list = None
    current_obj  = None

    for line in fm_text.splitlines():
        obj_field   = re.match(r'^    (\w+):\s*"?(.*?)"?\s*$', line)
        list_item   = re.match(r'^  - (.+)$', line)
        list_header = re.match(r'^(\w+):\s*$', line)
        kv          = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)

        if obj_field and current_obj is not None:
            current_obj[obj_field.group(1)] = obj_field.group(2)
        elif list_item and current_list is not None:
            item_text = list_item.group(1).strip().strip('"')
            sub_kv = re.match(r'(\w+):\s*"?(.*?)"?$', item_text)
            if sub_kv:
                current_obj = {sub_kv.group(1): sub_kv.group(2)}
                current_list.append(current_obj)
            else:
                current_list.append(item_text)
                current_obj = None
        elif list_header:
            current_list = []
            current_obj  = None
            meta[list_header.group(1)] = current_list
        elif kv:
            current_list = None
            current_obj  = None
            meta[kv.group(1)] = kv.group(2)

    return meta, body

# ── Math protection ───────────────────────────────────────────────────────────

def protect_math(text):
    placeholders = {}
    counter = [0]
    def store(m):
        key = f'XMATHX{counter[0]}XMATHX'
        counter[0] += 1
        placeholders[key] = m.group(0)
        return key
    text = re.sub(r'\$\$[\s\S]+?\$\$', store, text)
    text = re.sub(r'(?<!\$)\$(?!\$)(?:[^$\n]|\\.)+?(?<!\$)\$(?!\$)', store, text)
    return text, placeholders

def restore_math(text, placeholders):
    for key, val in placeholders.items():
        text = text.replace(key, val)
    return text

# ── Figure / video directives ─────────────────────────────────────────────────

DIRECTIVE_RE  = re.compile(r'^::(figure|video)\{([^}]*)\}\s*$', re.MULTILINE)
# figure-row block: ::figure-row{caption="..."} ... ::end-figure-row
ROW_RE        = re.compile(
    r'^::figure-row\{([^}]*)\}[ \t]*\n(.*?)\n::end-figure-row[ \t]*$',
    re.MULTILINE | re.DOTALL
)
# figure-block: groups multiple rows under one shared caption
# ::figure-block{caption="..."}
#   ::figure-row{} ... ::end-figure-row
#   ::figure-row{} ... ::end-figure-row
# ::end-figure-block
BLOCK_RE      = re.compile(
    r'^::figure-block\{([^}]*)\}[ \t]*\n(.*?)\n::end-figure-block[ \t]*$',
    re.MULTILINE | re.DOTALL
)
ITEM_RE       = re.compile(r'::(figure|video)\{([^}]*)\}')
FIG_SENTINEL  = 'XFIGSENTINELX'

def parse_attrs(s):
    return {m.group(1): m.group(2) for m in re.finditer(r'(\w+)="([^"]*)"', s)}

def inline_md(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text

def render_item_html(kind, attrs, include_caption=True):
    src = attrs.get('src', '')
    cap = attrs.get('caption', '') if include_caption else ''
    sub = attrs.get('subcaption', '')
    cap_html = f'\n  <div class="figure-caption">{inline_md(cap)}</div>' if cap else ''
    sub_html = f'\n  <div class="figure-subcaption">{inline_md(sub)}</div>' if sub else ''
    if kind == 'figure':
        media = f'  <img src="{html_module.escape(src)}" alt="{html_module.escape(cap or sub)}" loading="lazy">'
    else:
        media = (f'  <video autoplay loop muted playsinline>\n'
                 f'    <source src="{html_module.escape(src)}" type="video/mp4">\n'
                 f'  </video>')
    return media, sub_html, cap_html

def replace_directives(text):
    figures = []

    # 0. Handle ::figure-block (multiple rows, one shared caption)
    INNER_ROW_RE = re.compile(
        r'::figure-row\{([^}]*)\}[ \t]*\n(.*?)\n[ \t]*::end-figure-row',
        re.DOTALL
    )
    def block_replacer(m):
        block_attrs   = parse_attrs(m.group(1))
        block_body    = m.group(2)
        block_cap     = block_attrs.get('caption', '')
        block_cap_html = f'\n  <div class="figure-caption">{inline_md(block_cap)}</div>' if block_cap else ''

        rows_html = ''
        for rm in INNER_ROW_RE.finditer(block_body):
            row_body = rm.group(2)
            items_html = ''
            for im in ITEM_RE.finditer(row_body):
                kind  = im.group(1)
                attrs = parse_attrs(im.group(2))
                media, sub_html, _ = render_item_html(kind, attrs, include_caption=False)
                items_html += f'  <div class="fig-row-item">\n  {media}{sub_html}\n  </div>\n'
            rows_html += f'  <div class="fig-row fig-block-row">\n{items_html}  </div>\n'

        fig = f'<figure class="post-figure">\n{rows_html}{block_cap_html}\n</figure>'
        figures.append(fig)
        return f'\n\n{FIG_SENTINEL}{len(figures)-1}{FIG_SENTINEL}\n\n'

    text = BLOCK_RE.sub(block_replacer, text)

    # 1. Handle ::figure-row blocks
    def row_replacer(m):
        row_attrs    = parse_attrs(m.group(1))
        row_body     = m.group(2)
        row_cap      = row_attrs.get('caption', '')
        row_cap_html = f'\n  <div class="figure-caption">{inline_md(row_cap)}</div>' if row_cap else ''

        # optional aspect ratio e.g. ratio="16/9" or ratio="4/3"
        ratio = row_attrs.get('ratio', '')
        if ratio:
            try:
                w, h  = (float(x) for x in ratio.split('/'))
                pt    = round(h / w * 100, 4)
                ratio_attrs = f' data-ratio="{html_module.escape(ratio)}" style="--fig-ratio-pt:{pt}%"'
            except Exception:
                ratio_attrs = ''
        else:
            ratio_attrs = ''

        items_html   = ''
        for im in ITEM_RE.finditer(row_body):
            kind  = im.group(1)
            attrs = parse_attrs(im.group(2))
            media, sub_html, _ = render_item_html(kind, attrs, include_caption=False)
            items_html += f'  <div class="fig-row-item">\n  {media}{sub_html}\n  </div>\n'
        fig = (f'<figure class="post-figure">\n'
               f'  <div class="fig-row"{ratio_attrs}>\n{items_html}  </div>'
               f'{row_cap_html}\n</figure>')
        figures.append(fig)
        return f'\n\n{FIG_SENTINEL}{len(figures)-1}{FIG_SENTINEL}\n\n'

    text = ROW_RE.sub(row_replacer, text)

    # 2. Handle standalone ::figure / ::video
    def replacer(m):
        kind  = m.group(1)
        attrs = parse_attrs(m.group(2))
        media, _, cap_html = render_item_html(kind, attrs)
        figures.append(f'<figure class="post-figure">\n{media}{cap_html}\n</figure>')
        return f'\n\n{FIG_SENTINEL}{len(figures)-1}{FIG_SENTINEL}\n\n'

    text = DIRECTIVE_RE.sub(replacer, text)
    return text, figures

def split_on_sentinels(html, figures):
    pat   = re.compile(r'(?:<p>)?' + FIG_SENTINEL + r'(\d+)' + FIG_SENTINEL + r'(?:</p>)?')
    parts = pat.split(html)
    out   = []
    i     = 0
    while i < len(parts):
        chunk = parts[i].strip()
        if chunk:
            out.append(f'<div class="post-body">\n{chunk}\n</div>')
        i += 1
        if i < len(parts):
            out.append(figures[int(parts[i])])
            i += 1
    return '\n\n'.join(out)

# ── Template helpers ──────────────────────────────────────────────────────────

def authors_html(authors):
    if not authors:
        return ''
    rows = ''
    for a in authors:
        if isinstance(a, dict):
            name  = html_module.escape(a.get('name', ''))
            affil = a.get('affiliation', '')
            afsp  = f'<span class="author-affil"> · {html_module.escape(affil)}</span>' if affil else ''
            rows += f'<span class="author-item">{name}{afsp}</span>\n'
        else:
            rows += f'<span class="author-item">{html_module.escape(str(a))}</span>\n'
    return f'<div class="authors">\n{rows}</div>'

def links_html(links):
    if not links:
        return ''
    items = ''.join(
        f'<a class="hero-link" href="{html_module.escape(l.get("url","#"))}">'
        f'{html_module.escape(l.get("label","Link"))}</a>\n'
        for l in links if isinstance(l, dict)
    )
    return f'<div class="hero-links">\n{items}</div>' if items else ''

def abstract_html(abstract):
    return f'<p class="abstract">{html_module.escape(abstract)}</p>' if abstract else ''

# ── Main ──────────────────────────────────────────────────────────────────────

def convert(md_path, template_path, output_path):
    md_text  = Path(md_path).read_text(encoding='utf-8')
    template = Path(template_path).read_text(encoding='utf-8')

    meta, body   = parse_frontmatter(md_text)
    title        = meta.get('title', 'Blog Post')
    date         = meta.get('date', '')
    abstract     = meta.get('abstract', '')
    authors      = meta.get('authors', [])
    links        = meta.get('links', [])

    body, figures        = replace_directives(body)
    body, math_ph        = protect_math(body)

    md = markdown.Markdown(extensions=[
        'fenced_code', 'tables', 'footnotes', 'attr_list', 'pymdownx.superfences'
    ])
    content = md.convert(body)
    content = restore_math(content, math_ph)
    content = split_on_sentinels(content, figures)

    html = template
    html = html.replace('{{TITLE}}',         html_module.escape(title))
    html = html.replace('{{DATE}}',          html_module.escape(date))
    html = html.replace('{{AUTHORS_HTML}}',  authors_html(authors))
    html = html.replace('{{LINKS_HTML}}',    links_html(links))
    html = html.replace('{{ABSTRACT_HTML}}', abstract_html(abstract))
    html = html.replace('{{CONTENT}}',       content)

    Path(output_path).write_text(html, encoding='utf-8')
    print(f'✓  Written: {output_path}')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('input')
    p.add_argument('-o', '--output')
    p.add_argument('-t', '--template')
    args = p.parse_args()

    if not os.path.exists(args.input):
        sys.exit(f'Error: not found: {args.input}')
    output   = args.output   or str(Path(args.input).with_suffix('.html'))
    template = args.template or str(Path(__file__).parent / 'template.html')
    if not os.path.exists(template):
        sys.exit(f'Error: template not found: {template}')
    convert(args.input, template, output)

if __name__ == '__main__':
    main()
