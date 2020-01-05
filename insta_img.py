# # from instapy_cli import client
# # from textwrap import dedent
# # username = 'ritvikmehra0000' #your username
# # password = 'tensa zangetsu' #your password 
# # image='ww.jpg'

# # text=dedent("hello #py")
# # with client(username,password) as cli:
# #     cli.upload(image,text)   

# # from instapy_cli import client
# # username = 'ritvikmehra0000' #your username
# # password = 'tensa zangetsu' #your password 
# # image = 'ww.png' #here you can put the image directory
# # text = 'Here you can put your caption for the post' + '\r\n' + 'you can also put your hashtags #pythondeveloper #webdeveloper'
# # with client(username, password) as cli:
# # cli.upload(image, text)       

# # from instapy_cli import client
# # username = 'ritvikmehra0000' #your username
# # password = 'tensa zangetsu' #your password 
# # image = 'Hi_instagram.png' #here you can put the image directory
# # text = 'Here you can put your caption for the post' + '\r\n' + 'you can also put your hashtags #pythondeveloper #webdeveloper'
# # with client(username, password) as cli:
# #     cli.upload(image, text)        


# import urllib.request
# from PIL import Image, ImageOps
# from instapy_cli import client
# from datetime import date

# def get_item_shop():
#     url = "http://api2.nitestats.com/v1/shop/image?footer=USE%20CODE:%20%22DISTURBED%22"
#     urllib.request.urlretrieve(url, "ww.png")

# def resize():
#     desired_size = 1728
#     im_pth = "ww.png"

#     im = Image.open(im_pth)
#     old_size = im.size  # old_size[0] is in (width, height) format

#     ratio = float(desired_size)/max(old_size)
#     new_size = tuple([int(x*ratio) for x in old_size])
#     # use thumbnail() or resize() method to resize the input image
#     # thumbnail is a in-place operation
#     # im.thumbnail(new_size, Image.ANTIALIAS)
#     im = im.resize(new_size, Image.ANTIALIAS)
#     # create a new image and paste the resized on it

#     new_im = Image.new("RGB", (desired_size, desired_size), (30,30,30))
#     new_im.paste(im, ((desired_size-new_size[0])//2,
#                     (desired_size-new_size[1])//2))

#     output_path = 'ww.png2.jpg'
#     new_im.save(output_path)

# def post():
#     today = date.today()
#     d2 = today.strftime("%B %d, %Y")

#     heart = "\U00002764"

#     username = 'ritvikmehra0000'
#     password = 'ritvik99'
#     cookie_file = 'cookie.json'

#     image = 'ww.png'
#     text = 'Daily item shop for ' + d2 +'.' + '\r\n' + '\r\n' + 'Rate this item shop from 1-10!' + '\r\n' + '\r\n' + 'Use code: "Disturbed" to support me! ' + heart + '\r\n' + '#fortnite #ww #dailyww #fortniteww'


#     with client(username, password, cookie_file=cookie_file, write_cookie_file=True) as cli:

#         cookies = cli.get_cookie()

#         cli.upload(image, text)

# if __name__ == "__main__":
#     post()