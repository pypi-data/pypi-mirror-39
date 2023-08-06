import math
import re
import gym
import gym.spaces
import numpy as np
import collections


class InputInventory(collections.OrderedDict):
    def __init__(self, listofinputs=None):
        super(InputInventory, self).__init__()
        if listofinputs is not None:
            if type(listofinputs) is list and all([type(item) is list for item in listofinputs]):
                listofinputs = [item[1] for item in listofinputs]
            assert all([isinstance(item, CircuitInput) for item in listofinputs])
            listofinputs = sorted(listofinputs)
            for inpt in listofinputs:
                if inpt.instname:
                    self.update({inpt.instname: inpt})
                elif inpt.instname and inpt.subinstance:
                    self.update({inpt.instname + '.' + inpt.instparam: inpt})
                elif inpt.instparam and not inpt.instname:
                    self.update({inpt.instparam: inpt})
                else:
                    raise NotImplementedError


class ObservationDeck(collections.OrderedDict):
    def __init__(self, listofobservations=None):
        super(ObservationDeck, self).__init__()
        if listofobservations is not None:
            if type(listofobservations) is list and all([type(item) is list for item in listofobservations]):
                listofobservations = [item[1] for item in listofobservations]
            assert all([isinstance(item, CircuitObservation) for item in listofobservations])
            listofobservations = sorted(listofobservations)
            for obs in listofobservations:
                if obs.netname and not obs.instname and not obs.instpin:
                    self.update({obs.netname: obs})
                elif obs.instname and obs.instpin:
                    self.update({obs.instname + '.' + obs.instpin: obs})
                elif obs.instname and obs.netname:
                    self.update({obs.instname + '.' + obs.netname: obs})
                else:
                    raise NotImplementedError


class ObservationMapping(dict):
    def __init__(self, list_of_equivalencies=None):
        super(ObservationMapping, self).__init__()
        assert type(list_of_equivalencies) is list and all([type(item) is tuple for item in list_of_equivalencies])
        assert all([len(item) == len(list_of_equivalencies[0]) for item in list_of_equivalencies])
        for i, tupe in enumerate(list_of_equivalencies):
            for j, name in enumerate(tupe):
                self.update({name: list(set([item for item in tupe]))})


class CircuitInput(object):
    # Circuit Inputs define the interface between the Circuit and Python.
    #    levels - correspond to Python-side manifestation (i.e. integers, strings)
    #    values - correspond to Circuit-side manifestation (i.e. volts)

    def __init__(self,
                 nlevels=None, minlevel=None, maxlevel=None, current_level=None, initial_level=0,
                 nvalues=None, minvalue=None, maxvalue=None, current_value=None, initial_value=None,
                 action_mode=None, circuit_mode=None, action_space=None, action_gain=1.0,
                 random=False,
                 maxtimestep=None, datarate=None,
                 netname=None, instname=None, instparam=None, paramname=None, cname=None,
                 ):
        assert 'noopupdown' in action_mode \
               or 'integer' in action_mode \
               or 'discrete' in action_mode \
               or 'continuous' in action_mode, \
            'must provide either \'noopupdown,\' \'integer,\' \'discrete,\'' \
            ' or \'continuous\' for value of \'action_mode\''

        self.random = random
        self.netname = netname
        self.instname = instname
        self.instparam = instparam
        self.paramname = paramname
        self.cname = cname
        # self.sclobj = None

        self.minlevel = minlevel
        self.maxlevel = maxlevel
        self.nlevels = nlevels if nlevels is not None else maxlevel - minlevel + 1
        self.initial_level = initial_level
        self.current_level = current_level if current_level is not None else initial_level
        self.initial_value = initial_value if initial_value is not None else self.level2value(self.initial_level)
        self.current_value = current_value if current_value is not None else initial_value
        self.previous_val = initial_value
        self.nvalues = nvalues if nvalues is not None else self.nlevels
        self.maxvalue = maxvalue
        self.minvalue = minvalue
        self.value_range = self.maxvalue - self.minvalue
        self.value_step = self.value_range / (self.nvalues - 1)
        self.action_mode = action_mode
        self.maxtimestep = maxtimestep

        if action_space is not None:
            self.action_space = action_space
        else:
            if 'continuous' in self.action_mode:
                if 'centered' in self.action_mode:
                    self.action_space = gym.spaces.Box(low=np.array([-1.0]), high=np.array([1.0]), dtype=np.float16)
                else:
                    self.action_space = gym.spaces.Box(low=np.array([0.0]), high=np.array([1.0]), dtype=np.float16)
            else:
                self.action_space = gym.spaces.Discrete(self.nlevels)

    def action2level(self, action):
        raise NotImplementedError

    def level2value(self, level):
        raise NotImplementedError

    def apply_action(self, action):
        self.current_level = self.action2level(action)
        self.current_value = self.level2value(self.current_level)
        # self.set_spectre_values(circuit)
        # print('# current_level: {}'.format(self.current_level))

    def set_spectre_values(self, circuit, block=True):
        raise NotImplementedError

    def take_action(self, action, circuit):
        self.apply_action(action)
        self.set_spectre_values(circuit)

    def reset(self, circuit, block=True):
        self.apply_level(self.initial_level)
        self.previous_val = self.initial_value
        self.set_spectre_values(circuit, block=block)

    def apply_level(self, level):
        self.current_level = level
        self.current_value = self.level2value(self.current_level)

    def sample(self, seed=None):
        """Uniformly randomly sample a random element of this space.
        """
        return self.action_space.sample(seed=seed)

    def contains(self, x):
        """Return boolean specifying if x is a valid member of this space
        """
        return self.action_space.contains(x)

    def __lt__(self, other):
        return self.cname < other.cname


class PwlInput(CircuitInput):

    def __init__(self, instname=None, instparam=None, paramname=None, cname=None,
                 highvalue=None, lowvalue=None, initial_value=0.0, random=False,
                 steptime=None, nlevels=np.inf, risetime=1e-12, action_mode='continuous', circuit_mode='continuous',
                 initial_level=0):

        self.instname = instname
        self.instparam = instparam
        self.paramname = paramname
        self.risetime = risetime
        self.steptime = steptime
        self.action_mode = action_mode  # continuous or discrete
        self.circuit_mode = circuit_mode  # continuous or discrete
        self.maxtimestep = steptime if steptime else risetime / 50.0
        self.highvalue = highvalue
        self.lowvalue = lowvalue
        self.random = random
        self.initial_value = initial_value
        self.initial_level = initial_level

        if not ('discrete' in action_mode or 'integer' in action_mode) \
                and not ('discrete' in circuit_mode or 'integer' in circuit_mode):
            self.nlevels = np.Inf

        else:
            self.nlevels = nlevels
            self.lsb = (self.highvalue - self.lowvalue) / (self.nlevels - 1)

        if instname and not instparam and not paramname:
            self.cname = instname
        elif instname and instparam and not paramname:
            self.cname = instname + '.' + instparam
        elif not instname and not instparam and paramname:
            self.cname = paramname

        super(PwlInput, self).__init__(
            instname=self.instname, instparam=self.instparam, paramname=self.paramname, cname=str(self.cname),
            nvalues=self.nlevels, minvalue=self.lowvalue, maxvalue=self.highvalue, initial_value=self.initial_value,
            initial_level=self.initial_level, nlevels=self.nlevels, maxtimestep=float(self.maxtimestep),
            datarate=self.steptime, action_mode=self.action_mode, random=self.random)

    def action2level(self, action):
        assert action.size == 1
        if 'continuous' in self.action_mode and 'continuous' in self.circuit_mode:
            if 'centered' in self.action_mode:
                return (action + 1) / 2
            else:
                assert 0 <= action <= 1
                return action
        elif 'continuous' in self.action_mode and 'discrete' in self.circuit_mode:
            return np.round((action - self.minvalue) / self.lsb)
        elif 'discrete' in self.action_mode and 'discrete' in self.circuit_mode:
            assert isinstance(action, (int, np.integer))
            assert 0 <= action <= (self.nlevels - 1)
            return action
        elif 'discrete' in self.action_mode and 'continuous' in self.circuit_mode:
            assert 0 <= action <= (self.nlevels - 1)
            return np.int(action)
        else:
            raise NotImplementedError

    def level2value(self, level):
        if level is None and 'continuous' in self.action_mode:
            level = self.action2level(np.array(0))
        if not isinstance(level, np.ndarray):
            level = np.array(level)
        assert level.size == 1
        if 'continuous' in self.action_mode and 'continuous' in self.circuit_mode:
            return np.clip(level * (self.maxvalue - self.minvalue) + self.minvalue, self.minvalue, self.maxvalue)
        elif 'discrete' in self.action_mode and 'discrete' in self.circuit_mode:
            return level * self.lsb + self.minvalue
        elif 'continuous' in self.action_mode and 'discrete' in self.circuit_mode:
            return level * self.lsb + self.minvalue
        elif 'discrete' in self.action_mode and 'continuous' in self.circuit_mode:
            return level * self.lsb + self.minvalue
        else:
            raise NotImplementedError

    def set_spectre_values(self, circuit, block=True):
        t0 = circuit.simtime
        t1 = t0 + self.risetime
        t2 = t0 + self.maxtimestep
        simtype = circuit.internalsim.analysis_type
        if simtype == 'tran':
            valsvect = [-self.maxtimestep, self.previous_val, t0, self.previous_val, t1, self.current_value, circuit.sim_time_limit, self.current_value]
        elif simtype == 'envlp':
            valsvect = [-self.maxtimestep, self.previous_val, 0.0, self.previous_val, self.risetime, self.current_value, circuit.sim_time_limit, self.current_value]

        circuit.internalsim.setparams(
            self.cname,
            {'wave': valsvect },
            block=block,
        )
        self.previous_val = self.current_value
        return


class BitInput(CircuitInput):

    def __init__(self, instname=None, instparam=None, paramname=None, cname=None,
                 highvalue=None, lowvalue=None, initial_value=0, initial_level=0.0, random=False,
                 datarate=None, maxtimestep=None, action_mode='discrete'):
        self.width = 1
        self.nlevels = 2
        self.instname = instname
        self.instparam = instparam
        self.paramname = paramname
        self.datarate = datarate
        self.maxtimestep = maxtimestep if maxtimestep is not None else 1 / datarate
        self.cname = cname
        self.highvalue = highvalue
        self.lowvalue = lowvalue
        self.random = random
        self.initial_level = initial_level
        self.initial_value = initial_value if initial_value else self.level2value(self.initial_level)
        self.circuit_mode = 'discrete'

        super(BitInput, self).__init__(instname=instname, instparam=instparam, paramname=paramname, cname=cname,
                                       nvalues=2, minvalue=lowvalue, maxvalue=highvalue, initial_value=initial_value,
                                       nlevels=2, initial_level=initial_level, maxtimestep=maxtimestep,
                                       datarate=datarate, action_mode='integer', random=random)

    def action2level(self, action):
        assert action.size == 1
        return np.round(np.clip(action, 0, 1)).astype(int)

    def level2value(self, level):
        val = self.highvalue if level > 0 else self.lowvalue
        return val


class WordInput(CircuitInput):
    arraypattern = '<(\d+):(\d+)>$'

    def __init__(self,
                 instname=None, instparam=None, paramname=None,
                 initial_level=None, highvalue=None, lowvalue=None,
                 action_mode='discrete', action_gain=1.0,
                 datarate=None, random=False):

        self.cname = self.parsenamestrings(instname=instname, instparam=instparam, paramname=paramname)
        self.width = len(self.cname)
        self.nlevels = int(math.pow(2, self.width))
        self.datarate = datarate
        self.maxtimestep = 1 / self.datarate
        self.circuit_mode = 'discrete'
        self.action_mode = action_mode
        self.action_gain = action_gain
        self.highvalue = highvalue
        self.lowvalue = lowvalue
        self.random = random
        self.initial_level = initial_level
        self.current_level = initial_level
        self.initial_word = self.level2word(self.initial_level)
        self.bit = [BitInput(cname=name, initial_level=self.initial_word[self.cname.index(name)],
                             highvalue=highvalue, lowvalue=lowvalue, random=random,
                             maxtimestep=self.maxtimestep, datarate=self.datarate) for name in self.cname]

        super(WordInput, self).__init__(instname=instname, instparam=instparam, paramname=paramname,
                                        cname=self.cname, nlevels=self.nlevels, action_mode=self.action_mode,
                                        action_gain=self.action_gain,
                                        maxlevel=self.nlevels - 1, minlevel=0, initial_level=self.initial_level,
                                        maxvalue=self.highvalue, minvalue=self.lowvalue,
                                        datarate=self.datarate, maxtimestep=self.maxtimestep)

    def action2level(self, action):
        return np.clip(action, self.minlevel, self.maxlevel).astype(int).tolist()

    def level2word(self, level):
        word = np.binary_repr(level)
        if len(word) < self.width:
            word = word.zfill(self.width)
        return np.array(list(word)).astype(int)

    def word2value(self, word):
        value = [self.bit[idx].level2value(word[idx]) for idx in range(len(word))]
        return value

    def level2value(self, level):
        return self.word2value(self.level2word(level))

    def set_spectre_values(self, circuit):
        reversed_values = self.current_value[::-1]
        for idx in range(len(self.bit)):
            self.bit[idx].current_level = self.current_level
            self.bit[idx].current_value = reversed_values[idx]
            self.bit[idx].set_spectre_values(circuit)

    def parsenamestrings(self, instname=None, instparam=None, paramname=None):
        insearch = re.search(self.arraypattern, instname) if instname else None
        ipsearch = re.search(self.arraypattern, instparam) if instparam else None
        psearch = re.search(self.arraypattern, paramname) if paramname else None

        if not sum([insearch is not None, ipsearch is not None, psearch is not None]) == 1:
            raise IOError('when specifying a \'digital word\' circuit input, you must give either instname, '
                          'instparam, or paramname as a list or in the cadence vector '
                          'format: \"parameter_name<0:7>\"')

        if insearch:
            indices = range(int(insearch.group(1)), int(insearch.group(2)) + 1)
            basename = re.split(self.arraypattern, instname)[0]
            instname = [basename + str(index) for index in indices]
            cnames = instname

        elif ipsearch:
            indices = range(int(ipsearch.group(1)), int(ipsearch.group(2)) + 1)
            basename = re.split(self.arraypattern, instparam)[0]
            instparam = [basename + str(index) for index in indices]
            cnames = instparam

        elif psearch:
            indices = range(int(psearch.group(1)), int(psearch.group(2)) + 1)
            basename = re.split(self.arraypattern, paramname)[0]
            paramname = [basename + str(index) for index in indices]
            cnames = paramname

        elif type(instname) is list:
            cnames = instname
        elif type(instparam) is list:
            cnames = [instname + '.' + p for p in instparam]
        elif type(paramname) is list:
            cnames = paramname
        else:
            raise IOError('can\'t figure out the individual bits of your word')

        if instname and ipsearch:
            cnames = [instname + '.' + chname for chname in cnames]

        return cnames


class AnalogInput(CircuitInput):
    slewrate = None
    bandwidth = None

    def __init__(self, instname=None, instparam=None, paramname=None,
                 nlevels=256, initlevel=0, minvalue=0, maxvalue=5,
                 bandwidth=1e6, maxslew=None, action_mode='noopupdown', random=False):

        CircuitInput.__init__(self,
                              instname=instname, instparam=instparam, paramname=paramname,
                              nlevels=nlevels, initial_level=initlevel, current_level=initlevel,
                              nvalues=nlevels, minvalue=minvalue, maxvalue=maxvalue,
                              action_mode=action_mode, random=random)

        if maxslew:
            self.slewrate = maxslew
            self.bandwidth = maxslew / (math.pi * self.value_range)

        elif bandwidth:
            self.bandwidth = bandwidth
            self.slewrate = self.value_range * math.pi * bandwidth
        self.maxtimestep = self.value_step / self.slewrate
        self.circuit_mode = 'continuous'

    def action2level(self, action):
        raise NotImplementedError

    def level2value(self, level):
        return self.minvalue + level * self.value_step


class CircuitObservation(gym.spaces.Box):
    def __init__(self, netname=None, instname=None, instpin=None,
                 minval=-np.inf, maxval=np.inf, mode='continuous'):
        assert mode == 'continuous' or mode == 'discrete'

        gym.spaces.Box.__init__(self, low=minval, high=maxval, shape=(1,), dtype=np.float16)

        self.mode = mode
        self.netname = netname
        self.instname = instname
        self.instpin = instpin
        if self.netname:
            self.cname = self.netname
        elif self.instname and self.instpin:
            self.cname = '.'.join([self.instname, self.instpin])

    def __lt__(self, other):
        return self.netname < other.netname