import sys
import os
import re
from glob import glob

from ..core.helpers import console

appPat = '^([a-zA-Z0-9_-]+)$'
appRe = re.compile(appPat)


# COMMAND LINE ARGS

def getDebug(cargs=sys.argv):
  for arg in cargs[1:]:
    if arg == '-d':
      return True
  return False


def getCheck(cargs=sys.argv):
  for arg in cargs[1:]:
    if arg == '-c':
      return True
  return False


def getNoweb(cargs=sys.argv):
  for arg in cargs[1:]:
    if arg == '-noweb':
      return True
  return False


def getDocker(cargs=sys.argv):
  for arg in cargs[1:]:
    if arg == '-docker':
      return True
  return False


def getLocalClones(cargs=sys.argv):
  for arg in cargs[1:]:
    if arg == '-lgc':
      return True
  return False


def getModules(cargs=sys.argv):
  for arg in cargs[1:]:
    if arg.startswith('--mod='):
      return arg
  return ''


def getSets(cargs=sys.argv):
  for arg in cargs[1:]:
    if arg.startswith('--sets='):
      return arg
  return ''


def getParam(cargs=sys.argv, interactive=False):
  myDir = os.path.dirname(os.path.abspath(__file__))
  dataSourcesParent = getAppDir(myDir, '')
  dataSourcesPre = glob(f'{dataSourcesParent}/*/config.py')
  dataSources = set()
  for p in dataSourcesPre:
    parent = os.path.dirname(p)
    d = os.path.split(parent)[1]
    match = appRe.match(d)
    if match:
      app = match.group(1)
      dataSources.add(app)
  dPrompt = '/'.join(dataSources)

  dataSource = None
  for arg in cargs[1:]:
    if arg.startswith('-'):
      continue
    dataSource = arg
    break

  if interactive:
    if dataSource is None:
      dataSource = input(f'specify data source [{dPrompt}] > ')
    if dataSource not in dataSources:
      console('Unknown data source', error=True)
      dataSource = None
    if dataSource is None:
      console(f'Pass a data source [{dPrompt}] as first argument', error=True)
    return dataSource

  if dataSource is None:
    return None
  if dataSource not in dataSources:
    console('Unknown data source', error=True)
    return False
  return dataSource


# FIND THE APP DIREC~TORY

def getAppDir(myDir, dataSource):
  parentDir = os.path.dirname(myDir)
  tail = '' if dataSource == '' else dataSource
  return f'{parentDir}/apps/{tail}'


# HTML FORMATTING

def pageLinks(nResults, position, spread=10):
  if spread <= 1:
    spread = 1
  elif nResults == 0:
    lines = []
  elif nResults == 1:
    lines = [(1, )]
  elif nResults == 2:
    lines = [(1, 2)]
  else:
    if position == 1 or position == nResults:
      commonLine = (1, nResults)
    else:
      commonLine = (1, position, nResults)
    lines = []

    factor = 1
    while factor <= nResults:
      curSpread = factor * spread
      first = _coarsify(position - curSpread, curSpread)
      last = _coarsify(position + curSpread, curSpread)

      left = tuple(n for n in range(first, last, factor) if n > 0 and n < position)
      right = tuple(n for n in range(first, last, factor) if n > position and n <= nResults)

      both = tuple(n for n in left + (position, ) + right if n > 0 and n <= nResults)

      if len(both) > 1:
        lines.append(both)

      factor *= spread

    lines.append(commonLine)

  html = '\n'.join(
      '<div class="pline">' + ' '
      .join(f'<a href="#" class="pnav {" focus" if position == p else ""}">{p}</a>'
            for p in line) + '</div>'
      for line in reversed(lines)
  )
  return html


def passageLinks(passages, sec0, sec1):
  sec0s = []
  sec1s = []
  for s0 in passages[0]:
    selected = str(s0) == str(sec0)
    sec0s.append(f'<a href="#" class="s0nav {" focus" if selected else ""}">{s0}</a>')
  if sec0:
    for s1 in passages[1]:
      selected = str(s1) == str(sec1)
      sec1s.append(f'<a href="#" class="s1nav {" focus" if selected else ""}">{s1}</a>')
  return f'''
  <div class="sline">
    {''.join(sec0s)}
  </div>
  <div class="sline">
    {''.join(sec1s)}
  </div>
'''


# FORM VALUES

def getValues(options, form):
  values = {}
  for (option, default, typ, acro, desc) in options:
    value = form.get(option, None)
    if typ == 'checkbox':
      value = True if value else False
    values[option] = value
  return values


def setValues(options, source, form, emptyRequest):
  for (option, default, typ, acro, desc) in options:
    # only apply the default value if the form is empty
    # if the form is not empty, the absence of a checkbox value means
    # that the checkbox is unchecked
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/checkbox
    value = source.get(option, default if emptyRequest else None)
    if typ == 'checkbox':
      value = True if value else False
    form[option] = value


def shapeOptions(options, values):
  html = []
  for (option, default, typ, acro, desc) in options:
    value = values[option]
    if typ == 'checkbox':
      value = 'checked' if value else ''
    else:
      value = f'value="{value}"'
    html.append(
        f'''
      <div>
        <input
          class="r" type="{typ}" id="{acro}" name="{option}" {value}
        /> <span class="ilab">{desc}</span>
      </div>'''
    )
  return '\n'.join(html)


def shapeCondense(condenseTypes, value):
  html = []
  lastType = len(condenseTypes) - 1
  for (i, (otype, av, b, e)) in enumerate(condenseTypes):
    checked = ' checked ' if value == otype else ''
    radio = (
        '<span class="cradio">&nbsp;</span>'
        if i == lastType else f'''<input class="r cradio" type="radio" id="ctp{i}"
              name="condenseTp" value="{otype}" {checked}
            "/>'''
    )
    html.append(
        f'''
    <div class="cline">
      {radio}
      <span class="ctype">{otype}</span>
      <span class="cinfo">{e - b + 1: 8.6g} x av length {av: 4.2g}</span>
    </div>
  '''
    )
  return '\n'.join(html)


def shapeFormats(textFormats, value):
  html = []
  for (i, fmt) in enumerate(textFormats):
    checked = ' checked ' if value == fmt else ''
    radio = (
        f'''<input class="r tradio" type="radio" id="ttp{i}"
              name="textformat" value="{fmt}" {checked}
            "/>'''
    )
    html.append(
        f'''
    <div class="tfline">
      {radio}
      <span class="ttext">{fmt}</span>
    </div>
  '''
    )
  return '\n'.join(html)


# LOWER LEVEL

def _coarsify(n, spread):
  nAbs = int(round(abs(n) / spread)) * spread
  return nAbs if n >= 0 else -nAbs
