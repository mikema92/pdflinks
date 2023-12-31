from os import path
from glob import glob

delimiter = '_'
# finds and returns a list of all files sorted alphabetically that ends in extension ext 
def find_files_with_ext(dr, ext, ig_case=True):
    print(f"find_ext: finding all files with ext [.{ext}] in folder [{dr}]...")
    if ig_case:
        ext =  "".join(["[{}]".format(ch + ch.swapcase()) for ch in ext])  
    files = glob(path.join(dr, "*." + ext))
    files.sort()
    print(f"find_ext: found files [{files}]")
    return files

def get_filename(filepath, ext):
    filepart = filepath.split('/')[-1]

    fname = filepart[:-len(ext)-1]
    fnamepart = fname.split(delimiter)
    if len(fnamepart) == 1:
        return fname
    return ''.join(fnamepart[1:])

if __name__ == "__main__":
    # This code will only be executed 
    # if the script is run as the main program
    files = find_ext(".", "py")
    for f in files:
        fname = get_filename(f, "py")
        print(fname)