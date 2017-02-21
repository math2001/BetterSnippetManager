# -*- encoding: utf-8 -*-

class templates:
    pass

templates.xml = """\
<snippet>
    <content><![CDATA[
{content}
]]></content>
    <tabTrigger>{trigger}</tabTrigger>
    <scope>{scopes}</scope>
    <description>{description}</description>
</snippet>
"""

templates.sane = """\
---
tabTrigger: {trigger}
scope: {scopes}
description: {description}
---
{content}
"""
