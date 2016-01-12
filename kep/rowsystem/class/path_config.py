def current_folder():
    curpath = os.path.realpath(__file__)
    return os.path.dirname(curpath)

def level_up(path, n = 1):
    for i in range(n):
        path = os.path.split(path)[0]
    return path

REPO_ROOT_FOLDER = level_up(current_folder(), n = 3)
CURRENT_MONTH_DATA_FOLDER = os.path.join(REPO_ROOT_FOLDER, 'data', '2015', 'ind11')
