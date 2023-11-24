#!/usr/bin/env python3

import sys
import requests
import os

GIGAPROMPT_API_KEY = os.environ["GIGAPROMPT_API_KEY"]

SYSTEM = ("You are a git expert and developer with communication "
          "skills. You are praised for following best practices and writing "
          "legible comments.")

PROMPT = (
    "Write a high quality commit message for the previous git diff output.\n"
    "A good commit message has a title, then a newline, and up to 3 short "
    "sentences. The sentences must carry the overview and the 'why' of the commit."
)


def complete(diff):
    r = requests.post(
        "https://gigaprompt-xi.vercel.app/api/completions/sagemaker",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GIGAPROMPT_API_KEY}"
        },
        json={
            "messages": [{
                "role": "system",
                "content": SYSTEM
            }, {
                "role": "user",
                "content": f"{diff}\n---\n{PROMPT}"
            }],
            "endpoint":
            "chatml-alfred-v2-sft-ep-2023-10-30-13-57-26",
            "region":
            "us-west-2",
            "maxTokens":
            500,
            "temperature":
            0.3
        })

    return r.content.decode()


def label(diff, good_msg, bad_msg):
    URL = "https://gigaprompt-xi.vercel.app/api/feedbacks"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GIGAPROMPT_API_KEY}",
    }

    payload = {
        "promptJson": [
            {
                "role": "system",
                "content": SYSTEM
            },
            {
                "role": "user",
                "content": f"{diff}\n---\n{PROMPT}"
            },
        ],
        "type":
        "git-commit",
        "bestContinuation":
        good_msg,
        "worstContinuation":
        bad_msg,
    }

    response = requests.post(URL, json=payload, headers=headers)


if __name__ == "__main__":
    if sys.argv[1] == "complete":
        print(complete(open(sys.argv[2]).read()))
    elif sys.argv[1] == "label":
        diff = open(sys.argv[2]).read()
        good_file = open(sys.argv[3])
        bad_file = open(sys.argv[4])
        label(diff, good_file.read(), bad_file.read())
    else:
        print("Unknown command")
        sys.exit(1)
