import re
import sys

# Used to remove internal wiki links cancellation :
# https://code.google.com/p/support/wiki/WikiSyntax#Internal_wiki_links
project_name = "GwtQuery"


def convert_to_md(wiki_file):
    with open(wiki_file) as f:
        wiki = f.read()

    wiki = remove_gplusone(wiki)
    wiki = remove_toc(wiki)
    wiki = remove_internal_wiki_link_cancellations(wiki)
    wiki = convert_links(wiki)
    wiki = convert_code_snippets(wiki)
    wiki = convert_numbered_lists(wiki)
    wiki = convert_headers(wiki)

    return wiki


def remove_gplusone(wiki):
    return re.sub(r"<g:plusone.*</g:plusone>", "", wiki)


def remove_toc(wiki):
    return re.sub(r"<wiki:toc.*/>", "", wiki)


def remove_internal_wiki_link_cancellations(wiki):
    return wiki.replace("!{}".format(project_name), project_name)


def convert_links(wiki):
    return re.sub(r"\[(http.*) (.*)\]", r"[\2](\1)", wiki)


def convert_code_snippets(wiki):
    return wiki.replace("{{{", "\n```").replace("}}}", "```\n")


def convert_numbered_lists(wiki):
    return wiki.replace("# ", "1. ")


def convert_headers(wiki):
    wiki = re.sub(r"====== ?(.*[^ ]) ?======", r"###### \1", wiki)
    wiki = re.sub(r"===== ?(.*[^ ]) ?=====", r"##### \1", wiki)
    wiki = re.sub(r"==== ?(.*[^ ]) ?====", r"#### \1", wiki)
    wiki = re.sub(r"=== ?(.*[^ ]) ?===", r"### \1", wiki)
    wiki = re.sub(r"== ?(.*[^ ]) ?==", r"## \1", wiki)
    wiki = re.sub(r"= ?(.*[^ ]) ?=", r"# \1", wiki)

    wiki = replace_summary(wiki)

    return wiki


def replace_summary(wiki):
    """If there is a #summary tag, set all headers one level below (e.g. # -> ##) and set #summary as h1"""
    if "#summary" in wiki:
        wiki = wiki.replace("# ", "## ")
        wiki = wiki.replace("#summary", '#')
    return wiki


if __name__ == '__main__':
    print(convert_to_md(sys.argv[1]))
