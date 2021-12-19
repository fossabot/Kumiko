FROM python:3.10.1
WORKDIR /Bot
COPY Pipfile ./ /Bot/
COPY Pipfile.lock ./ /Bot/
RUN pip install --upgrade pip pipenv
RUN pipenv install
EXPOSE 4002
CMD ["pipenv", "run", "python", "./Bot/rinbot.py"]
