# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['markdown_image_caption']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'markdown-image-caption',
    'version': '0.2.1',
    'description': 'Image caption support for Python Markdown',
    'long_description': '# Markdown Image caption.\n\nInspired by the probably un-maintained package [mdx_figcap](ttps://github.com/mkszk/mdx_figcap)\n\n## Usage:\n\nMake sure you have [markdown](https://pypi.org/project/Markdown/) installed. \n\nDefine an image with caption in your markdown.\n\n```markdown\n![alttext](http://example.com/image.png "caption")\n```\n\nThis will be converted to:\n\n```html\n\n<span class="img_container center" style="display: block;">\n    <img alt="test" src="http://example.com/image.png" style="display:block; margin-left: auto; margin-right: auto;" title="caption" />\n    <span class="img_caption" style="display: block; text-align: center;">caption</span>\n</span>\n```\n\nWhy no figure tag implementation ?\n\nThe figure tag is a block level element. The image element is an inline element. This difference breaks the attribute extension.\nSo `![alttext](http://example.com/image.png "caption"){: .center}` would not work if a figure was used.\n\n## Installation\n\n```bash\npip install markdown-image-caption\n```\n\nadd the plugin to your markdown\n\n```python\nimport markdown\n\nparser = markdown.Markdown(extensions=["markdown_image_caption.plugin"])\n```',
    'author': 'Sander Teunissen',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
