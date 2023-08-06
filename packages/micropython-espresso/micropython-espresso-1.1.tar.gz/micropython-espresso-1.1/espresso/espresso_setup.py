BOOT = '/boot.py'

activated = "import espresso"
deactivated = "# import espresso"

# Read current boot status
with open(BOOT, 'r') as file:
    content = file.read()


# ----------------------------------------------------------------------
def enable():
    """"""
    content = content.replace(deactivated, '')
    content = content.replace(activated, '')

    with open(BOOT, 'r') as file:
        file.write('\n{}'.format(activated))


# ----------------------------------------------------------------------
def disable():
    """"""
    content = content.replace(deactivated, '')
    content = content.replace(activated, '')

    with open(BOOT, 'r') as file:
        file.write('\n{}'.format(deactivated))

