# Instalatiom
```sh
pip install webbrowserdownloader
```
# Downloader
### Basic functional
```python
from webbrowserdownloader import Browser
browser = Browser()
page_content = browser.get_page('https://www.google.com/')
len(page_content)
```
### Proxies usage
```python
from webbrowserdownloader import Browser
browser = Browser(proxy_string='157.152.145.103:3128')
page_content = browser.get_page('https://www.google.com/')
````
# License
MIT
