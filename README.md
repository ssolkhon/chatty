# Chatty

ChatGPT AI assistant.

I built this to play around with the OpenAI API.

![Tests](https://github.com/ssolkhon/chatty/actions/workflows/tests.yaml/badge.svg)

### Usage:
You will be prompted for a question in your console:

```bash
Please ask Chatty a question...
```

The program will detect when you have finished asking your question and it will
then submit it to ChatGPT for a response. The response will then be spoken 
back to you. This is currently only tested on a Mac.

After each response you will be prompted to ask another question.

Once you are finished say "goodbye" and the program will end.

### Dependencies:
```bash
$ python3 -m 'venv' venv
$ source venv/bin/activate
$ pip install requirements.txt
```

### Run:
```bash
$ pip install .
$ export OPENAI_API_TOKEN=<Your-Token>
$ chatty
```

### Test:
```bash
$ pip install tox
$ tox
```

