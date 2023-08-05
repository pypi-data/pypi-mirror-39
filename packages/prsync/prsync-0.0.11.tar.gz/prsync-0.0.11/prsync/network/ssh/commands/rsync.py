def rsync_exists():
    return "rsync --version"


def rsync(flags, include_paths, exclude_paths, dest_host, dest_username, root_path, dest_path):
    root_path = root_path + ("." if root_path.endswith("/") else "/.")
    return "rsync {} {} {} {} {}@{}:{}".format(
        " ".join(flags),
        '--include="' + '" --include="'.join(include_paths) +'"' if len(include_paths) > 0 else '',
        '--exclude="' +'" --exclude="'.join(exclude_paths) +'"' if len(exclude_paths) > 0 else '',
        root_path,
        dest_username,
        dest_host,
        dest_path
    )

