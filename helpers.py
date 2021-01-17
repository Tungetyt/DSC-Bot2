def read_file(file_name):
    with open(f"{file_name}.txt") as rs:
        return rs.read().splitlines()
