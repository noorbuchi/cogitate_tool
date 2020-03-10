"""
Collects repository data for contributors of the master branch of a repo.

Writes the data to a .json file.

Calculates statistics based on the data from Github.

Steps to run data_collection.py and display the data table:

Must be in the repository folder

Run the python file using `pipenv run python src/data_collection.py`

Enter the name of the json file you want the data to be written to.

If prompted, due to data not being collected previously, enter the URL or path

of the Repository you would like to analyze.

If the current repository is the one you would like to analyze, simply

hit enter wihtout typing anything.
"""
from __future__ import division
import os
from pydriller import RepositoryMining
from prettytable import PrettyTable
from github import Github
import json_handler


def authenticate_repository(user_token, repository_name):
    """Authenticate the Github repository using provided credentials."""
    # Credentials for PyGithub functions and methods
    ghub = Github(user_token)
    repository = ghub.get_repo(repository_name)

    return repository


# Written as a temporary pass-through in case this variable is converted to a global
# variable, in which case that process would occur here. Pass-through will be eliminated
# during refactoring.
def initialize_contributor_data(file_path):
    """Load a dictionary based upon the given .json file."""
    contributor_data = json_handler.get_dict_from_json_file(file_path)

    return contributor_data


def retrieve_issue_data(repository, state, contributor_data):
    """Retrieve a contributor's involvement based upon issues and pull request threads."""
    issues = repository.get_issues(state=state)

    for issue in issues:
        for comment in issue.get_comments():
            if comment.user.login in contributor_data.keys():
                if issue.pull_request is None:
                    contributor_data[comment.user.login]["issues_commented"].append(
                        issue.number
                    )
                else:
                    contributor_data[comment.user.login][
                        "pull_requests_commented"
                    ].append(issue.number)
            else:
                contributor_data[comment.user.login] = {
                    "issues_commented": [],
                    "pull_requests_commented": [],
                    "issues_opened": [],
                    "pull_requests_opened": [],
                }
                if issue.pull_request is None:
                    contributor_data[comment.user.login]["issues_commented"].append(
                        issue.number
                    )
                else:
                    contributor_data[comment.user.login][
                        "pull_requests_commented"
                    ].append(issue.number)

        if issue.user.login in contributor_data.keys():
            if issue.pull_request is None:
                contributor_data[issue.user.login]["issues_opened"].append(issue.number)
            else:
                contributor_data[issue.user.login]["pull_requests_opened"].append(
                    issue.number
                )

    return contributor_data


def collect_commits_hash(repo):
    """Create a list of dictionaries that contains commit info.

    hash (str): hash of the commit
    msg (str): commit message
    author_name (str): commit author name
    author_email (str): commit author email
    author_date (datetime): authored date
    merge (Bool): True if the commit is a merge commit
    added: number of lines added
    removed: number of lines removed
    nloc: Lines Of Code (LOC) of the file
    complexity: Cyclomatic Complexity of the file
    methods: list of methods of the file.
    filename: files modified by commit.
    filepath: filepaths of files modified by commit.
    """
    commit_list = []

    for commit in RepositoryMining(repo).traverse_commits():

        line_added = 0
        line_removed = 0
        line_of_code = 0
        complexity = 0
        methods = []
        filename = []
        filepath = []

        for item in commit.modifications:
            # modifications is a list of files and its changes
            line_added += item.added
            line_removed += item.removed
            if item.nloc is not None:
                line_of_code += item.nloc
            if item.complexity is not None:
                complexity += item.complexity

            for method in item.methods:
                methods.append(method.name)
            filename.append(item.filename)
            filepath.append(item.new_path)

        single_commit_dict = {
            "hash": commit.hash,
            "author_msg": commit.msg,
            "author_name": commit.author.name,
            "author_email": commit.author.email,
            # "author_date": commit.author_date,
            "merge": commit.merge,
            "line_added": line_added,
            "line_removed": line_removed,
            "lines_of_code": line_of_code,
            "complexity": complexity,
            "methods": methods,
            "filename": filename,
            "filepath": filepath,
        }

        commit_list.append(single_commit_dict)

    return commit_list


def get_commit_average(lines, commits):
    """Find average lines modified per commit."""
    # Loop through the dictionary and calculate the average lines per commits
    # formula for average: (added + deleted)/number_of_commits
    if commits != 0:
        average = lines / commits
        return (int)(average)
    return 0


def parse_for_type(name):
    """Parse through file name and returns its format."""
    if "." in name:
        file_type, name = os.path.splitext(name)
        file_type += ""
        return name
    return name


def get_file_formats(files):
    """Create a list of unique file formats."""
    formats = []
    for file in files:
        current_format = parse_for_type(file)
        if current_format not in formats:
            formats.append(current_format)
    # sort data to ensure consistency for test
    formats = sorted(formats)
    return formats


# This function simplifies gathering and writing raw data to json file
# pylint: disable=C0330
def collect_and_add_raw_data_to_json(
    path_to_repo, json_file_name="raw_data_storage", overwrite=True
):
    """Use collect_commits_hash to collect data from the repository path.

    Overwrite any data in the chosen file unless otherwise specified.

    Default file is raw_data_storage unless otherwise specified.
    """
    # collects data from collect_commits_hash and reformat dicitionary
    raw_data = {"RAW_DATA": collect_commits_hash(path_to_repo)}
    # Write raw data to .json file
    # Checks if overwriting the file was picked
    if overwrite:
        # use json handler to overwrite the old content
        json_handler.write_dict_to_json_file(raw_data, json_file_name)
    else:
        # use json handler to update the old content
        json_handler.add_entry(raw_data, json_file_name)


# pylint: disable=C0330
def collect_and_add_individual_metrics_to_json(
    read_file="raw_data_storage",
    write_file="individual_metrics_storage",
    overwrite=True,
):
    """Use calculate_individual_metrics to calculate metrics using read_file.

    Write metrics to write_file.

    Overwrite existing data in write_file unless otherwise specified.
    """
    # Call calculate_individual_metrics to get data dicitionary
    metrics = calculate_individual_metrics(read_file)
    # Write raw data to .json file
    # Checks if overwriting the file was picked
    if overwrite:
        # use json handler to overwrite the old content
        json_handler.write_dict_to_json_file(metrics, write_file)
    else:
        # use json handler to update the old content
        json_handler.add_entry(metrics, write_file)


def calculate_individual_metrics(json_file_name="raw_data_storage"):
    """Retrieve the data from .json file and create a dictionary keyed by user."""
    # retreive data from raw data json
    current_data = json_handler.get_dict_from_json_file(json_file_name)
    # creates a dictionary where the key is the authors username
    data_dict = {}
    # Check if RAW_DATA is in json tp prevent a key error
    if "RAW_DATA" in current_data.keys():
        for commit in current_data["RAW_DATA"]:
            author = commit["author_name"]
            email = commit["author_email"]
            # NOTE check date compatibility with json
            # check if the key already in in the dicitionary
            if author in data_dict:
                # condition passed, adds one to the number of commits
                data_dict[author]["COMMITS"] += 1
            else:
                # condition fails, creates a new key and adds empty data
                data_dict[author] = {
                    "EMAIL": email,
                    "COMMITS": 1,
                    "ADDED": 0,
                    "REMOVED": 0,
                    "TOTAL": 0,
                    "MODIFIED": 0,
                    "RATIO": 0,
                    "FILES": [],
                    "FORMAT": [],
                    "issues_commented": [],
                    "issues_opened": [],
                    "pull_requests_commented": [],
                    "pull_requests_opened": [],
                }

            data_dict[author]["ADDED"] += commit["line_added"]
            data_dict[author]["REMOVED"] += commit["line_removed"]
            # check if the explored file is not in the list in index seven
            current_files = commit["filename"]
            # add the current_files to the user files list without duplicates
            data_dict[author]["FILES"] = list(
                set(data_dict[author]["FILES"]) | set(current_files)
            )
            # Sort list to ensure consistency when testing
            data_dict[author]["FILES"] = sorted(data_dict[author]["FILES"])
        return data_dict
    # if RAW_DATA key was not found, empty dictionary will be returned
    return {}
    # NOTE: for printing the data please use the file print_table.py


def print_individual_in_table(
    file_name="individual_metrics_storage",
    headings=["EMAIL", "COMMITS", "ADDED", "REMOVED"],
):
    """Create and print the table using prettytable."""
    # Default headings are mentioned above in the parameter
    dictionary = json_handler.get_dict_from_json_file(file_name)
    # Initialize a PrettyTable instance
    data_table = PrettyTable()
    # add the username as a category for teh headings
    data_table.field_names = ["Username"] + headings
    # Loop through every author in the dictionary
    for author in dictionary:
        # Add the authors name to the current row
        current_row = [author]
        for heading in headings:
            # add the value from every heading to the current row
            current_row.append(dictionary[author][heading])
        # add row to prettytable instance
        data_table.add_row(current_row)
        # reset the current row to an empty list for the next iteration
        current_row = []
    print(data_table)


def find_repositories(repo):
    """Locates a Github repository with the URL provided by the user."""
    # ask the user for a URL of a Github repository
    miner = RepositoryMining(path_to_repo=repo)
    return miner


# TODO: needs revised
# def merge_duplicate_usernames(current_data, kept_entry, removed_entry):
#     """Take input from user and merge data in entries then delete one."""
#     dictionary = current_data["INDIVIDUAL_METRICS"]
#     categories = [
#         "COMMITS",
#         "ADDED",
#         "REMOVED",
#         "FILES",
#         "issues_commented",
#         "issues_opened",
#         "pull_requests_opened",
#         "pull_requests_commented",
#     ]
#     for category in categories:
#         # Special case for merging files to avoid duplicates
#         if category == "FILES":
#             dictionary[kept_entry][category] = list(
#                 set(dictionary[kept_entry][category])
#                 | set(dictionary[removed_entry][category])
#             )
#         else:
#             # simple addiyion for all other metrics
#             dictionary[kept_entry][category] += dictionary[removed_entry][category]
#     try:
#         del dictionary[removed_entry]
#     except KeyError:
#         print("Key 'testing' not found")
#     return {"INDIVIDUAL_METRICS": dictionary}


# This main method is only for the purposes of testing
if __name__ == "__main__":
    # NOTE: this supression needs to be resolved
    # pylint: disable=input-builtin
    # TODO: needs revised
    # FILE_NAME = input("Enter the name of the file to store data: ")
    # DATA = calculate_individual_metrics(FILE_NAME)
    # if DATA == {}:
    #     REPO_PATH = input("Enter repository path URL/Local: ")
    #     add_raw_data_to_json(REPO_PATH, FILE_NAME)
    #     print("processing data again")
    #     DATA = calculate_individual_metrics(FILE_NAME)
    # token = input("Enter user token")
    # repo_name = input("Enter repo name (org/repo_name): ")
    # current_repo = authenticate_repository(token, repo_name)
    # ISSUE_DATA = {}
    # ISSUE_DATA = retrieve_issue_data(current_repo, "all", ISSUE_DATA)
    # for key in ISSUE_DATA:
    #     if key not in DATA["INDIVIDUAL_METRICS"].keys():
    #         DATA["INDIVIDUAL_METRICS"][key] = {
    #             "EMAIL": "N/A",
    #             "COMMITS": 0,
    #             "ADDED": 0,
    #             "REMOVED": 0,
    #             "TOTAL": 0,
    #             "MODIFIED": 0,
    #             "RATIO": 0,
    #             "FILES": [],
    #             "FORMAT": [],
    #         }
    #     DATA["INDIVIDUAL_METRICS"][key].update(ISSUE_DATA[key])
    # print_individual_in_table(DATA)
    # choice = True
    # while choice:
    #     remove = input("enter username to be merged then deleted: ")
    #     keep = input("enter username to be merged into: ")
    #     DATA = merge_duplicate_usernames(DATA, keep, remove)
    #     print("data after this merge...")
    #     print_individual_in_table(DATA)
    #     pick = input("would you like to continue? y/n")
    #     if pick == "n":
    #         choice = False
    # # Write reformatted dictionary to json
    # json_handler.add_entry(DATA, FILE_NAME)
    # print_individual_in_table(DATA)

    # This call will use the default file names
    DATA = calculate_individual_metrics()
    # if statement will check if raw data was collected
    if DATA == {}:
        REPO_PATH = input("Enter the path to the repo : ")
        # This call will use default options for file and overwrite condition
        collect_and_add_raw_data_to_json(REPO_PATH)
    print("Adding processed data to selected json file...")
    collect_and_add_individual_metrics_to_json()
    print_individual_in_table()
