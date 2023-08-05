#!/usr/bin/env python
from walt.client.doc.markdown import MarkdownRenderer
from walt.client.doc.pager import Pager

with open('tutorial.md') as f:
    content = f.read().decode('utf-8')
renderer = MarkdownRenderer()
text = renderer.render(content)
pager = Pager()
pager.display(text)
