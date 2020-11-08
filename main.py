import json
import os
from datetime import datetime
from pytz import timezone
from helper.api import CodeWarsAPI
from helper.kata import KataParser
from extensions import file_extensions

with open('./setup.json') as fin:
    setup = json.load(fin)

with open('./source.html') as fin:
    file = fin.read()

base_dir = setup['export_dir']
tz_name = setup['timezone']

parser = KataParser(file)
katas = parser.parse_katas()
api = CodeWarsAPI(setup['api_key'])

commits = []

print('Exporting katas...')
for i, kata in enumerate(katas):
    print('\r{}/{} katas exported.'.format(i+1, len(katas)), end='')

    name, slug, url, description = api.get_kata(kata.kata_id())
    difficulty = kata.difficulty()
    solutions = zip(kata.language_ids(), kata.language_names(), kata.source_codes(), kata.times())

    kata_dir = os.path.join(base_dir, difficulty, slug)
    if not os.path.exists(kata_dir):
        os.makedirs(kata_dir)

    with open(os.path.join(kata_dir, 'README.md'), 'w') as fout:
        fout.write(description)

    for language_id, language_name, source_code, time in solutions:
        filename = 'solution-{}{}'.format(language_id, file_extensions.get(language_id, ''))
        with open(os.path.join(kata_dir, filename), 'w') as fout:
            fout.write(source_code)

        relative_dir = os.path.join(difficulty, slug)
        language_url = url + "/" + language_id
        commits.append((time, name, language_name, language_url, relative_dir, filename))
print()

with open('./git_commit.bash', 'w') as fout:
    fout.write('#!/bin/sh\n\n')
    fout.write('BASE={}\n\n'.format(base_dir))
    commits.sort(key=lambda tup: tup[0])
    for time, name, language_name, url, relative_dir, filename in commits:
        if tz_name != '':
            utc = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f%z')
            time = utc.astimezone(timezone(tz_name)).strftime('%Y-%m-%dT%H:%M:%S%z')
        fout.write(("git -C \"$BASE\"'{}{}' add '{}' README.md && " +
            "GIT_AUTHOR_DATE='{}' GIT_COMMITTER_DATE='{}' " +
            "git -C \"$BASE\" commit -m 'Solve \"{}\" in {}'$'\\n\\n''{}'\n")
                .format(os.sep, relative_dir, filename,
                    time, time, name, language_name, url))
