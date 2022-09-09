import re

if __name__ == "__main__":
    filename = "conc_temp.md"
    with open ("conclusion.md", "w") as tempfile:
        with open(filename, "r") as mdfile:
            lines = mdfile.readlines()

            for line in lines:
                line = line.replace("\n", " ")
                search_results = re.finditer("[\.\?\!]\s{1}", line)
                idxs = []
                for search_result in search_results:
                    idxs.append(search_result.span()[1])
                for idx in reversed(idxs):
                    line = line[:idx] + "\n" + line[idx:]

                if len(line) > 0 and not str.isspace(line):
                    tempfile.write(line)

    with open(filename, "r") as mdfile:
        lines = mdfile.readlines()

