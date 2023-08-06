from pexpect.replwrap import REPLWrapper
from .replwrap_parallel import REPLWrapper_client
import tempfile
import os.path
import shutil
import numpy as np
from .skill_interface import Accelerated_scl_interface
from . import Analyses
import signal
import sys
import libpsf
import re
from textwrap import wrap as textwrap
from shlex import split as shsplit


avail_output_modes = ['psfbin', 'nutmeg', 'psfascii', 'decida']
avail_readers = ['libpsf', 'decida']
float_fmt_string = '{:+13.6e}'


def format_float(float):
    return float_fmt_string.format(float)


def format_vect(vect):
    return ' '.join([float_fmt_string.format(v) for v in vect.T.flatten()])


class PwlInput(object):
    def __init__(self, name, max_n_points, parent=None):
        self.max_n_points = max_n_points
        self.cname = '.'.join(name, parent) if parent else name


class Pyspectre(object):

    def signal_handler(self, signal, frame):
        self.cleanup()
        raise KeyboardInterrupt

    def __del__(self):
        self.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        del self
        return

    def __init__(self,
                 netlist=None,
                 simdirectory=None,
                 analysis_name=None,
                 analysis_type=None,
                 spectre_output_mode=None,
                 spectre_reader='libpsf',
                 sourcefile=None,
                 spectre_binary='spectre',
                 spectre_env=None,
                 spectreargs=None,
                 logging=True,
                 delayed_start=False,
                 replwrap_client=False,
                 pwl_inputs=None
                 ):

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGABRT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        if not os.path.isfile(netlist):
            # print('netlist \"{}\" is not file'.format(netlist))
            # print('cwd: \"{}\"'.format(os.getcwd()))
            if not os.path.isdir(simdirectory):
                # print('simdirectory \"{}\" is not directory'.format(simdirectory))
                # print('cwd: \"{}\"'.format(os.getcwd()))
                raise IOError(
                    'unable to find spice netlist: netlist \"{}\" simdirectory: \"{}\"'.format(netlist, simdirectory))
            netlist = os.path.join(simdirectory, netlist)
            if not os.path.isfile(netlist):
                # print('netlist appended.  still not file: \"{}\"'.format(netlist))
                # print('cwd: \"{}\"'.format(os.getcwd()))
                raise IOError(
                    'unable to find spice netlist: netlist \"{}\" simdirectory: \"{}\"'.format(netlist, simdirectory))

        if not os.path.isdir(simdirectory):
            simdirectory = os.path.dirname(netlist)

        if spectreargs is not None:
            if isinstance(spectreargs, list):
                spectreargs = ' '.join(spectreargs)
            elif isinstance(spectreargs, str):
                spectreargs = spectreargs

        if pwl_inputs is not None:
            if isinstance(pwl_inputs, PwlInput):
                pwl_inputs = {pwl_inputs.cname, pwl_inputs}
            else:
                assert isinstance(pwl_inputs, list)
                assert all([isinstance(item, PwlInput) for item in pwl_inputs])
                pwl_inputs = {item.cname: item for item in pwl_inputs}

        self.spicefilepath = os.path.abspath(netlist)
        self.simdir = simdirectory
        self.replwrap_client = replwrap_client
        self.sourcefile = sourcefile
        self.analysis_name = analysis_name
        self.analysis_type = analysis_type
        self.spectre_binary = spectre_binary
        self.spectre_env = spectre_env
        self.spectreargs = spectreargs
        self.spectre_reader = spectre_reader
        self.logging = logging
        self.pwl_inputs = pwl_inputs

        self.dcsolution = None
        self.resultsdir = None
        self.quit = False
        self.spectre = None
        self.interface = None
        self.fresh = True

        self.resolve_spectre_modes(spectre_output_mode, spectre_reader)

        os.makedirs('/dev/shm/pyspectre', exist_ok=True) if not os.path.isdir('/dev/shm/pyspectre') else None

        cmd = [
            self.spectre_binary,
            '-64',
            '+interactive=skill',
            '-log -note -info -debug -warn -error ++aps=moderate',
            '-format={}'.format(self.spectre_output_mode),
            '-mt'
        ]

        if self.spectreargs:
            cmd.append(self.spectreargs)

        if self.logging:
            cmd.append('+log=\"spectre.log\"')

        self.basecmd = ' '.join(cmd)

        if self.pwl_inputs is not None:
            self.extend_pwl_defs_in_netlist()
        self.spectre = None
        if not delayed_start:
            self.startbinary()

        ## delaying the starting of the binary so this __init__ can be parallelized !!!!!!!!!!!!!!!!
        #
        # try:
        #     self.analysis_type = self.interface.listanalysis()[self.analysis_name]
        # except KeyError:
        #     raise RuntimeError('no analysis in netlist by the name:{}'.format(pyspectre_obj.analysis_name))
        # #self.analysis.init(self)

    def startbinary(self, block=True):
        if self.spectre is not None and self.spectre.child.isalive:
            return None
        if self.quit:
            return None

        # for item in os.listdir(self.simdir):
        #     if os.path.isfile(item):
        #         shutil.copyfile(item, self.resultsdir)
        #     elif os.path.isdir(item):
        #         shutil.copytree(item, self.resultsdir)

        self.resultsdir = tempfile.mkdtemp(dir='/dev/shm/pyspectre', prefix='')
        for item in [self.simdir + '/' + item for item in os.listdir(self.simdir)]:
            if item == self.spicefilepath:
                continue
            if os.path.isfile(item):
                shutil.copy(item, self.resultsdir)
            elif os.path.isdir(item):
                shutil.copytree(item, self.resultsdir + '/' + item.split('/')[-1], symlinks=True)
        shutil.copy(self.spicefilepath, self.resultsdir)

        # ahdldir = '/AHDL/{}'.format(self.spicefilepath.split('/')[-1].split('.')[0])
        ahdldir = '/AHDL/'

        self.cmd = 'cd ' + self.resultsdir \
                   + ' && ' + self.basecmd \
                   + ' -outdir=\"{}\"'.format(self.resultsdir) \
                   + ' -raw=\"{}\"'.format(self.resultsdir + '/psf') \
                   + ' -ahdllibdir=\"{}\"'.format(self.simdir + ahdldir) \
                   + ' ' + self.spicefilepath
        # + ' ' + self.spicefilepath.split('/')[-1]

        if self.sourcefile:
            self.cmd = 'source ' + self.sourcefile + '; ' + self.cmd

        # self.cmd = self.cmd.insert(0, 'CDS_AHDLCMI_SIMDB_DIR=\"' + self.ahdldir + '\"')
        # self.cmd = self.cmd.insert(0, 'CDS_AHDLCMI_SHIPDB_COPY=yes')
        # os.environ['CDS_AHDLCMI_SIMDB_DIR'] = self.ahdldir+'/shipdb'
        # os.environ['CDS_AHDLCMI_SHIPDB_DIR'] = self.ahdldir+'/shipdb'
        # os.environ['CDS_AHDLCMI_SHIPDB_COPY'] = 'YES'

        if self.spectre_env is not None:
            ### don't use dict here, becuase we're sensitive to order... must execute in order
            if type(self.spectre_env) is tuple:
                assert len(self.spectre_env) % 2 == 0
                self.spectre_env = [(self.spectre_env[i], self.spectre_env[i + 1]) for i in
                                    range(0, len(self.spectre_env), 2)]
            assert type(self.spectre_env) is list and all([type(item) is tuple for item in self.spectre_env])
            for (var, value) in self.spectre_env:
                os.environ[var] = os.path.expandvars(value)

        try:
            if self.replwrap_client:
                self.spectre = REPLWrapper_client(
                    'bash --noprofile --norc -c \'' + self.cmd + '\'',
                    b'\n> '.decode('unicode-escape'),
                    None)
                self.spectre.launch_spectre(block=block)
                self.fresh = False

            else:

                self.spectre = REPLWrapper(
                    'bash --noprofile --norc -c \'' + self.cmd + '\'',
                    b'\n> '.decode('unicode-escape'),
                    None
                )
                self.fresh = False
                self.spectre.child.delayafterclose = 0.0
                self.spectre.child.delaybeforesend = 0.0
                self.spectre.child.delayafterread = 0.0
                self.spectre.child.delayafterterminate = 0.0

            self.interface = Accelerated_scl_interface(self)
            self.pid = int(self.spectre.child.pid)
            self.commandct = 0
            if block or isinstance(self.spectre, REPLWrapper):
                self.resolve_analysis_type()

        except BaseException as e:
            if self.spectre is not None:
                print(self.spectre.child.before)
            self.cleanup()
            raise e
        return

    def extend_pwl_defs_in_netlist(self):
        if self.pwl_inputs is None:
            return
        targets = [item.cname for item in self.pwl_inputs.values()]
        target_names = [item.split('.')[-1] for item in targets]

        netlist = open(self.spicefilepath, mode='r').read().splitlines()

        # go through and find definitions:
        def_lines = {}
        context = []
        for line_no, line in enumerate(netlist):
            line = line.lstrip()
            if line.startswith('//'):
                continue
            toks = line.split()
            if len(toks) < 1:
                continue
            anchor = toks[0]
            if anchor == 'subckt':
                context.append(toks[1])
                continue
            if anchor == 'ends':
                context.pop()
                continue
            if anchor in target_names:
                this_guys_name = '.'.join(context) + '.' + anchor if context else anchor
                if this_guys_name in targets:
                    stopline = line_no
                    while re.match(r'.*\\\s*$', netlist[stopline]):
                        stopline += 1
                    def_lines.update({this_guys_name: {'range': range(line_no, stopline + 1)}})

        assert all([item in def_lines for item in targets])

        file_pattern = r'^.*(\s+file\s*=\s*\".+?\")'
        wave_pattern = r'^.*(\s+wave\s*=\s*\".+?\")'

        for name, patch_dict in def_lines.items():

            fulldef = ' '.join([netlist[ll].replace('\\', '').strip() for ll in patch_dict['range']])

            # remove all 'file' definitions

            if re.match(file_pattern, fulldef):
                fulldef = ' '.join(
                    [item.strip() for item in fulldef.split(re.match(file_pattern, fulldef).groups()[0])]).strip()

            # check and extend existing 'wave' definition
            if re.match(wave_pattern, fulldef):
                oldwave = re.match(wave_pattern, fulldef).groups()[0].split('=')[1].strip().strip('\"').split()
                fulldef = ' '.join(
                    [item.strip() for item in fulldef.split(re.match(wave_pattern, fulldef).groups()[0])]).strip()
                old_time = np.stack([float(t) for t in oldwave[::2]])
                old_vals = np.stack([float(v) for v in oldwave[1::2]])

                if old_time.size >= self.pwl_inputs[name].max_n_points:
                    continue
                else:
                    aug_len = self.pwl_inputs[name].max_n_points - old_time.size
                    ts = np.max(np.diff(old_time))
                    new_time = np.concatenate(
                        [old_time, np.linspace(old_time[-1] + ts, old_time[-1] + aug_len * ts, aug_len)])
                    new_vals = np.concatenate([old_vals, np.random.randn(aug_len)])

                    newval_str = ' '.join(
                        [' '.join([float_fmt_string] * 2).format(new_time[i], new_vals[i]) for i in range(aug_len)])

            else:
                # create brand-new 'wave' definition
                aug_len = self.pwl_inputs[name].max_n_points
                ts = 1
                new_time = np.linspace(0, (aug_len - 1) * ts, aug_len)
                new_vals = np.random.randn(aug_len)

                newval_str = ' '.join(
                    [' '.join([float_fmt_string] * 2).format(new_time[i], new_vals[i]) for i in range(aug_len)])

            fulldef = ' '.join([fulldef, 'wave=[' + newval_str + ']'])
            fulldef = textwrap(fulldef, break_long_words=False, break_on_hyphens=False, subsequent_indent='    ')
            fulldef[:-1] = [item + ' \\' for item in fulldef[:-1]]  ## fwd slash on ends of lines
            # fulldef[1:] = ['+ ' + item for item in fulldef[1:]]     ## '+' at beginning of lines
            def_lines[name].update({'def': [ll + '\n' for ll in fulldef]})

        # all fixed up!
        # shutil.copy(self.spicefilepath, self.spicefilepath+'_bk')
        patchlist = [item['range'] for item in def_lines.values()]

        with open(self.spicefilepath + '_alt', mode='w') as outfile:
            for line_no, line in enumerate(netlist):
                if any([line_no in r for r in patchlist]):
                    patch = [v for v in def_lines.values() if line_no in v['range']][0]
                    if line_no + 1 not in patch['range']:
                        outfile.writelines(patch['def'])
                        del patchlist[patchlist.index(patch['range'])]
                else:
                    outfile.write(line + '\n')
        self.spicefilepath = self.spicefilepath + '_alt'

    def resolve_analysis_type(self):
        self.analysis_type = self.interface.listanalysis()[self.analysis_name]
        self.analysis = eval('Analyses.' + self.analysis_type.title() + '()')

    def getparams(self, obj, paramnames):
        if isinstance(paramnames, str):
            paramnames = [paramnames]
        paramlist = self.interface.listparams(obj)
        assert all([name in paramlist for name in paramnames]), 'coudln\'t find parameter named:{} in object:{}'.format(
            name, obj)
        return {name: self.interface.getparametervalue(obj, name) for name in paramnames}

    def setparams(self, obj, paramdict, block=True):
        assert isinstance(paramdict, dict)
        for name, value in paramdict.items():
            self.interface.setparametervalue(obj, name, value, block=block)

    def setpwl(self, name, time, volts):

        if isinstance(name, PwlInput):
            name = name.cname

        assert len(time.shape) <= 2
        if len(time.shape) == 2:
            assert np.min(time.shape) == 1
            time = time.flatten()

        assert len(volts.shape) <= 2
        if len(volts.shape) == 2:
            assert np.min(volts.shape) == 1
            volts = volts.flatten()

        assert time.shape == volts.shape

        as_text = '[' + format_vect(np.stack([time, volts])) + ']'

        self.setparams(name, {'wave': as_text})

    def resolve_spectre_modes(self, spectre_output_mode, spectre_reader):
        if spectre_output_mode is None and spectre_reader is None:
            self.spectre_output_mode = 'psfbin'
            self.spectre_reader = 'libpsf'

        elif spectre_reader is not None and spectre_output_mode is None:
            assert spectre_reader in avail_readers
            self.spectre_reader = spectre_reader
            if spectre_reader == 'decida':
                self.spectre_output_mode = 'nutascii'
            elif spectre_reader == 'libpsf':
                self.spectre_output_mode = 'psfbin'
            else:
                raise NotImplementedError

        elif spectre_output_mode is not None and spectre_reader is None:
            assert spectre_output_mode in avail_output_modes
            self.spectre_output_mode = spectre_output_mode
            if spectre_output_mode == 'ascii':
                self.spectre_reader = 'nutascii'
            elif spectre_output_mode == 'psfbin':
                self.spectre_reader = 'libpsf'
            else:
                raise NotImplementedError

        else:
            assert spectre_reader in avail_readers
            self.spectre_reader = spectre_reader
            assert spectre_output_mode in avail_output_modes
            self.spectre_output_mode = spectre_output_mode

    def cleanup(self):
        self.quit = True
        try:
            self.interface.quit()
        except:
            try:
                self.spectre.child.terminate()
            except:
                try:
                    self.spectre.child.kill(9)
                except:
                    try:
                        os.kill(self.pid, 9)
                    except:
                        pass
        try:
            shutil.rmtree(self.resultsdir)
        except:
            pass

    def wait(self):
        if isinstance(self.spectre, REPLWrapper_client):
            self.spectre.wait()
        else:
            return

    def runanalysis(self, block=True):
        self.interface.runanalysis(self.analysis_name, block=block)

    def setresultsdir(self, relpath):
        self.interface.setresultsdir(relpath)

    def readstatefile(self, filename=None):
        statedata = {}
        with open(os.path.join(self.resultsdir, filename)) as rdata:
            for line in rdata:
                if line.startswith('#'):
                    continue
                else:
                    tok = line.split()
                    statedata.update({tok[0]: float(tok[1])})

        return statedata

    def readdcfile(self):
        return self.readstatefile(self.analysis.dcfile)

    def readtranfile(self):
        return self.readstatefile(self.analysis.tranfile)

    def init(self, *args, **kwargs):
        """ use this for one-time calls which will persist forever"""
        self.analysis.init(self, *args, **kwargs)
        return self.analysis.dcfile

    def reset(self, *args, **kwargs):
        """ use this for one-time prep calls which will persist between analyses"""
        self.analysis.reset(self, *args, **kwargs)
        return self.analysis.tranfile

    def step(self, *args, **kwargs):
        """ use this for calls which have to be made before every step"""
        self.analysis.step(self, *args, **kwargs)
        return self.analysis.tranfile

    def copydc2tran(self):
        shutil.copyfile(
            os.path.join(self.resultsdir, self.analysis.dcfile),
            os.path.join(self.resultsdir, self.analysis.tranfile))

    def get_data(self, signames=None):
        if isinstance(signames, (str)):
            signames = [signames]

        x = []
        t = []

        t, x = self.analysis.interpret_data(self, signames)
        return t, x

    def read_file(self, filename, signames):
        if not os.path.isfile(filename):
            filename = os.path.join(self.resultsdir, 'psf', filename)

        if self.spectre_reader == 'libpsf':
            try:
                d = libpsf.PSFDataSet(filename)
            except IOError as e:
                print(
                    'ERROR: libpsf couldn\'t open file: '
                    '{}. See spectre simulation directory: {}'.format(filename, self.resultsdir)
                )
                raise e

            return d.get_sweep_values().flatten(), np.array([d.get_signal(signame) for signame in signames])

        else:
            raise NotImplementedError
