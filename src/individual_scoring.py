import operator

# For 3/3/2020:
# TODO Fake data - start with dictionary - Madelyn *
# TODO function for commit score - Teona *
# TODO function for added lines score - Teona *
# TODO function for deleted lines - Wonjoon *
# TODO lines modified score - Madelyn *
# TODO lines per commit score - Wonjoon *
# TODO amount of files modified overall score - Madelyn *
# TODO file for printing the individual score - Teona *
# TODO average of all scores - Everyone, once other features are finished

# Possible other features or scoring metrics:
# TODO amount of files per commit score
# TODO talk about using PyGithub to retrieve issue data
# TODO amount of comments in lines of code score - research tools for parsing
# TODO date distribution score
# TODO average overall score and individual score to produce new individual score
# TODO give notification of duplicate username if there is one, or the possibility
# User inputs the weight for each category for finding total individual score

# Helpful reminders:
# Use pipeline programming style
# Implement test cases as functions are written in the test_individual_scoring.py file
# Scoring will be done first as percentages ((individual contribution/total branch)*100)

# Add fake data that corresponds to overall-eval-analyzing-metrics branch
# github_data uses the pattern ["username", commit_total, lines_added,
# lines_deleted, total_lines, modified_lines, lines_per_commit, files_changed]


# NOTE This is the fake data, it does not have key for the email for now, for tesing purposes
github_data = {
"noorbuchi" : {"COMMITS" : 28, "ADDED" : 349, "REMOVED" : 70},
"bagashvilit" : {"COMMITS" : 22, "ADDED" : 355, "REMOVED" : 56},
"Jordan-A" : { "COMMITS" : 23, "ADDED" : 375, "REMOVED" : 43},
"WonjoonC": { "COMMITS" : 27, "ADDED" : 365, "REMOVED" : 67},
"Hannah Schultz": { "COMMITS" : 25, "ADDED" : 315, "REMOVED" : 75},
"Alexander_Hamilton": { "COMMITS" : 41, "ADDED" : 350, "REMOVED" : 54},
"Karl_Marx": { "COMMITS" : 0, "ADDED" : 0, "REMOVED" : 0},
"Julius_Caesar": { "COMMITS" : 25, "ADDED" : 363, "REMOVED" : 35},
"Napoleon_Bonaparte": { "COMMITS" : 24, "ADDED" : 540, "REMOVED" : 2},
"Alexander_the_Great": { "COMMITS" : 42, "ADDED" : 355, "REMOVED" : 50},
}

# NOTE: The following code block still needs to be fixed in terms of variable
# names and docstrings.
def percentage(individual,overal_branch):
    """Function to calculate the individual contribution percentage"""
    return round(individual * 100 / overal_branch)

def sum_value(key):
    """Function to sum up all the values in branch per key"""
    return sum(d[key] for d in github_data.values() if d)

def individual_commitmnet(username,category):
    """Function to return value for key"""
    return github_data[username][category]

# Print usename and percentage of their contribution for each category
for username, data in github_data.items():
    print("\n",username)
    for category in data:
        print(category, percentage(individual_commitmnet(username,category),sum_value(category)),"%")