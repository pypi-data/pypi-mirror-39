# code referenced from: https://stackoverflow.com/a/30888321


def tar_extract(file_name):
    """
    This function extracts a compressed .tar or .tar.gz file.

    :param file_name: File name to extract.
    :type file_name: str.
    :return: None
    """
    import tarfile
    if file_name.endswith("tar.gz"):
        tar = tarfile.open(file_name, "r:gz")
        tar.extractall()
        tar.close()
    elif file_name.endswith("tar"):
        tar = tarfile.open(file_name, "r:")
        tar.extractall()
        tar.close()
