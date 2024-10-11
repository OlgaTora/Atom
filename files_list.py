import os


class FileNamesLoader:
    def __init__(self, files_dir: str):
        self.files_dir = files_dir

    def get_files_list(self) -> list | None:
        """
        Function for walk for directory with files
        :return: list of files ready to split
        """
        files_to_process = []
        for address, dirs, files in os.walk(self.files_dir):
            for name in files:
                files_to_process.append(os.path.join(address, name))
        if files_to_process:
            return files_to_process
        else:
            return None
