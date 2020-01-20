# -*- encoding: utf-8 -*-


class templates:
    pass


templates.xml = """\
<snippet>
\t<content><![CDATA[
{content}
]]></content>
\t<tabTrigger>{trigger}</tabTrigger>
\t<scope>{scopes}</scope>
\t<description>{description}</description>
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
