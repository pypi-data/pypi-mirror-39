from cdx_toolkit.cli import main

import json
import sys

import pytest
import requests


def test_basics(capsys):
    args = '--cc --limit 10 iter commoncrawl.org/*'.split()
    main(args=args)
    out, err = capsys.readouterr()

    split = out.splitlines()
    assert len(split) == 10
    for line in out.splitlines():
        # this might be commoncrawl.org./ or commoncrawl.org/
        assert 'commoncrawl.org' in line


def test_multi(capsys, caplog):
    tests = [
        [{'service': '--cc', 'mods': '--limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 10, 'linefgrep': 'commoncrawl.org'}],
        [{'service': '--cc', 'mods': '--limit 11', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 11, 'linefgrep': 'commoncrawl.org'}],
#        [{'service': '--cc', 'mods': '--limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/thisurlneverdidexist'},
#         {'count': 0}],  # should limit to 1 index because it runs slowly!
        [{'service': '--cc', 'mods': '--cc-mirror https://index.commoncrawl.org/ --limit 11', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 11, 'linefgrep': 'commoncrawl.org'}],
        [{'service': '--cc', 'mods': '--limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/* --all-fields'},
         {'count': 10, 'linefgrep': 'digest '}],
        [{'service': '--cc', 'mods': '--limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/* --fields=digest,length,offset --csv'},
         {'count': 11, 'csv': True}],
        [{'service': '--cc', 'mods': '--limit 10 --filter=status:200', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 10, 'linefgrep': 'status 200'}],
        [{'service': '--cc', 'mods': '--limit 10 --filter=!status:200', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 10, 'linefgrepv': 'status 200'}],
        [{'service': '--cc', 'mods': '--limit 10 --to=2017', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 10, 'linefgrep': 'timestamp 2017'}],
        [{'service': '--cc', 'mods': '--limit 10 --from=2017 --to=2017', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 10, 'linefgrep': 'timestamp 2017'}],
        [{'service': '--cc', 'mods': '--limit 3 --get --closest=20170615', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 3, 'linefgrep': 'timestamp 20170'}],  # data-dependent, and kinda broken
        [{'service': '--cc', 'mods': '--limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/* --csv'},
         {'count': 11, 'csv': True}],
        [{'service': '--cc', 'mods': '--limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/* --jsonl'},
         {'count': 10, 'jsonl': True}],
        [{'service': '--cc', 'mods': '-v -v --limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 10, 'debug': 5}],

        [{'service': '--ia', 'mods': '--limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 10, 'linefgrep': 'commoncrawl.org'}],
        [{'service': '--ia', 'mods': '--limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/thisurlneverdidexist'},
         {'count': 0}],
        [{'service': '--ia', 'mods': '--limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/* --all-fields'},
         {'count': 10, 'linefgrep': 'mime ', 'linefgrepv': 'original '}],  # both of these are renamed fields
        [{'service': '--ia', 'mods': '--get --limit 4 --closest=20170615', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 4, 'linefgrep': 'timestamp '}],  # returns 2008 ?! bug probably on my end
        [{'service': '--ia', 'mods': '-v -v --limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 10, 'debug': 5}],

        [{'service': '--source https://web.archive.org/cdx/search/cdx', 'mods': '--limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'count': 10, 'linefgrep': 'commoncrawl.org'}],
        [{'service': '-v -v --source https://web.arc4567hive.org/cdx/search/cdx', 'mods': '--limit 10', 'cmd': 'iter', 'rest': 'commoncrawl.org/*'},
         {'debug': 15, 'exception': requests.exceptions.ConnectionError}],  # 9 lines for the non-fail case, many more for fail

        [{'service': '--cc', 'mods': '--limit 10', 'cmd': 'size', 'rest': 'commoncrawl.org/*'},
         {'count': 1, 'is_int': True}],
        [{'service': '--ia', 'mods': '--limit 10', 'cmd': 'size', 'rest': 'commoncrawl.org/*'},
         {'count': 1, 'is_int': True}],
    ]

    for t in tests:
        inputs = t[0]
        outputs = t[1]
        cmdline = '{} {} {} {}'.format(inputs['service'], inputs['mods'], inputs['cmd'], inputs['rest'])
        args = cmdline.split()

        if 'exception' in outputs:
            with pytest.raises(outputs['exception']):
                main(args=args)
        else:
            main(args=args)

        out, err = capsys.readouterr()

        assert err == '', cmdline
        lines = out.splitlines()
        if 'count' in outputs:
            assert len(lines) == outputs['count'], cmdline
        for line in lines:
            if 'linefgrep' in outputs:
                assert outputs['linefgrep'] in line, cmdline
            if 'linefgrepv' in outputs:
                assert outputs['linefgrepv'] not in line, cmdline
            if 'csv' in outputs:
                assert line.count(',') >= 2, cmdline
            if 'jsonl' in outputs:
                assert line.startswith('{') and line.endswith('}'), cmdline
                assert json.loads(line), cmdline
            if 'is_int' in outputs:
                assert line.isdigit(), cmdline

        if 'debug' in outputs:
            assert len(caplog.records) > outputs['debug'], cmdline


def test_warc(tmpdir, caplog):
    # crash testing only, so far

    base = ' --limit 10 warc commoncrawl.org/*'
    full_suffix = '--prefix FOO --subprefix BAR --size 1 --creator creator --operator bob --url-fgrep common --url-fgrepv bar'

    prefixes = ('-v -v --cc', '--ia',
                '--cc --cc-mirror https://index.commoncrawl.org/',
                '--source https://web.archive.org/cdx/search/cdx --wb https://web.archive.org/web')

    with tmpdir.as_cwd():
        for p in prefixes:
            cmdline = p + base
            print(cmdline, file=sys.stderr)
            args = cmdline.split()
            main(args=args)

        cmdline = prefixes[0] + base + ' ' + full_suffix
        print(cmdline, file=sys.stderr)
        args = cmdline.split()
        main(args=args)
        assert True
