def list_files(path):
    """ changing to the given path, return the pwd (current path) + ls(including hidden files)   """
    return 'cd {}; pwd; ls -a'.format(path)

def build_path(new_path, old_path):
    """
     old path = the last path state
     new path = the new path based the old path

     i.e:
        old path = this/is/current/path
        new path = ..
        result will be this/is/current

        old path = this/is/current/path
        new path = dir
        result will be this/is/current/dir
     """
    if  old_path.endswith("/"):
        old_path = old_path[:-1]

    if new_path == "..":  # user climbed up
        old_path = old_path.rsplit('/', 1)[0]
    elif old_path == "/":  # root folder
        old_path += "{}/".format(new_path)
    else:  # add folder to path
        old_path += "/{}".format(new_path)

    if old_path == "":
        old_path = "/"

    return old_path