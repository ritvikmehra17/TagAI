from instapy_cli import client
from textwrap import dedent
username='ritvikmehra0000'
password='tensa zangetsu'
image='img_20191228120752.jpg'

text=dedent("""
            hello #py""")
with client(username,password) as cli:
    cli.upload(image,text)              