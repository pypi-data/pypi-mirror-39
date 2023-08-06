BOOT = '/boot.py'

activated = "import espresso"
deactivated = "# import espresso"

# Read current boot status
with open(BOOT, 'r') as file:
    content = file.read()


# ----------------------------------------------------------------------
def espresso_enable():
    """"""
    global content

    content = content.replace(deactivated, '')
    content = content.replace(activated, '')

    with open(BOOT, 'r') as file:
        file.write('\n{}'.format(activated))


# ----------------------------------------------------------------------
def espresso_disable():
    """"""
    global content

    content = content.replace(deactivated, '')
    content = content.replace(activated, '')

    with open(BOOT, 'r') as file:
        file.write('\n{}'.format(deactivated))

