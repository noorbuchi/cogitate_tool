"""Command Line Interface for the Cogitate tool."""

import argparse
import validators

# from web_interface import web_interface
import data_collection


def main():
    """Execute the CLI."""
    args = retrieve_arguments()

    # Currently only validates the PyGithub repository
    repository = data_collection.authenticate_repository(args["token"], args["repo"])

    # Temporary structure given issue retrieval is the only function
    contributor_data = data_collection.initialize_contributor_data(
        "contributor_data_template"
    )
    contributor_data = data_collection.retrieve_issue_data(
        repository, args["state"], contributor_data
    )
    link_str = str(args["link"])
    if link_validator(link_str) is True:
        data_collection.collect_commits_hash(args["link"])
    else:
        print("The link you have entered is invalid.")
    # gives the user the option to use the web interface
    web = True
    # while loop to ensure user input is "y" or "n"
    while web is True:
        # pylint: disable=input-builtin
        visit_web = input("Would you like to view the data on the web?(y/n)")
        if visit_web == "y":
            # print(web_interface.web_interface())
            print("link")
            web = False
        elif visit_web == "n":
            data_collection.print_file("contributor_data", ["repo"])
            # exits loop when user chooses not to use the web interface
            web = False
        else:
            print("Please enter (y/n).")
            # loop is repeated when output is not "y" or "n"
    print("Thank you for using GatorCogitate. Have a great day!")
    # end of the CLI main method


def retrieve_arguments():
    """Retrieve the user arguments and return the args dictionary."""
    # As no other functions exist in master as of this pull request, the args
    # below are written to accomadate issual retrieval in data_collection.py

    a_parse = argparse.ArgumentParser()
    a_parse.add_argument("-l", "--link", help="Cogitate a repo by the url of the repo")
    a_parse.add_argument(
        "-t", "--token", required=True, type=str, help="Github User Token"
    )
    a_parse.add_argument(
        "-r", "--repo", required=True, type=str, help="User's Repository"
    )
    a_parse.add_argument(
        "-s", "--state", required=False, type=str, help="State of the Issue"
    )

    args = vars(a_parse.parse_args())

    # pprint(find_repositories(args["link"]))

    return args


def team():
    """Call all team-based funtions."""


def individual():
    """Call all individual functions."""


def link_validator(url_str):
    """Take a string and checks if it is a valid URL."""
    # returns a boolean value
    return validators.url(url_str)


if __name__ == "__main__":
    main()
