import os
import glob
#
# print(f'\nFound these image files in current working directory\nDetected Possible Icons:')
#
# options = {}
# extensions = [".png", ".icns", ".ico"]
#
# count = int()
#
# for ext in extensions:
#     files = glob.glob(os.getcwd() + '/**/*' + ext, recursive=True)
#     options.update({count:files})
#     count += 1


# for key, value in enumerate(options[iter]):
#     print(f'[{str(key)}]: {str(value)}')
#

# for x in options:
#     print(f'[{x}]: {options.get(x)}')

# print(options)


# choice = int(input("choose icon: "))
#
# if int(choice) in range(1,4):
#     for key, value in enumerate(options):
#         if value == choice:
#             print(options.get(1))
# else:
#     print("Not an option!")

cool = input("give bundle id pls: ")
while "." not in cool:
    uSure = input("u need dot u sure to pass? N/y: ")
    if uSure in "Nn":
        continue
    elif uSure in "Yy":
        break
    else:
        continue
else:
    pass
