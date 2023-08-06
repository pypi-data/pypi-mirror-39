from __future__ import print_function

import gym
import numpy as np
from pyspectre import Pyspectre
import circuitgym.spaces
import multiprocessing as mp
import shutil
import os
import signal
import time
from .experience import _write_experience_file


class CircuitArray(gym.Env):
    metadata = {'render.modes': ['human']}

    def signal_handler(self, signal, frame):
        if hasattr(self, 'circuits'):
            for ckt in self.circuits:
                if hasattr(ckt, 'close'):
                    ckt.close()
        raise KeyboardInterrupt

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __init__(self,
                 filenames=None,
                 analysis_name=None,
                 result_name=None,
                 spectre_args=None,
                 spectre_source=None,
                 spectre_binary='spectre',
                 spectre_env=None,
                 simdirs=None,
                 input_inventories=None,
                 input_equivalency_map=None,
                 observation_decks=None,
                 observation_equivalency_map=None,
                 sim_time_limit=None,
                 max_n_steps=None,
                 rewardfunction=None,
                 plotfunction=None,
                 transient_time_resolution=None,
                 hyperthreading=False,
                 logging=False,
                 cache_enabled=False,
                 cache_level=3,
                 multidiscrete2discrete=False,
                 pyspectre_client=False,
                 replwrap_client=False,
                 datalog=False,
                 datalog_filename='cglog',
                 datalog_max_rows=300,
                 augmentors=None,
                 ):

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGABRT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        if isinstance(filenames, list) and all([os.path.isfile(filename) for filename in filenames]):
                # full paths given
                nckts = len(filenames)
                simdirs = [os.path.split(filename)[0] for filename in filenames]
        elif isinstance(filenames, list) and isinstance(simdirs, list):
                assert len(filenames) == len(simdirs)
                if all([os.path.isfile(os.path.join(dirname,filename)) for (dirname,filename) in zip(simdirs,filenames)]):
                    nckts = len(filenames)
        elif isinstance(filenames, list) and isinstance(simdirs, str):
            nckts = len(filenames)
            simdirs = [simdirs] * nckts
        elif isinstance(filenames, str) and isinstance(simdirs, list):
            nckts = len(simdirs)
            filenames = [filenames] * nckts
        else:
            raise ValueError('Circuit array must have either multiple filenames in same dir; multiple dirs; or both')

        self.ncircuits = nckts
        self.hyperthreading = hyperthreading
        self.logging = logging
        self.rewardfunction = rewardfunction
        self.reward_range = rewardfunction(get_limits=True)
        self.max_n_steps = max_n_steps
        self.cache_enabled = cache_enabled
        self.cache_level = cache_level
        self.multidiscrete2discrete=multidiscrete2discrete
        self.pyspectre_client = pyspectre_client
        self.replwrap_client = replwrap_client
        self.launched = False
        self.augmentors=augmentors if isinstance(augmentors,list) and len(augmentors)==self.ncircuits else [list() for i in range(self.ncircuits)]

        # #### data
        if datalog is not False:
            self._init_datalogging(datalog, datalog_filename, datalog_max_rows)

        # #### plotting stuff:
        self.figure = None
        self.ax1 = None
        self.figuredata = None
        self.plotfunction = plotfunction

        # #### setup circuits:
        self.circuits = nckts * [None]
        self.state = None
        if type(input_inventories) is not list:
            input_inventories = [input_inventories]*nckts

        if type(observation_decks) is list:
            if not all([observation_decks[0].keys() == item.keys() for item in observation_decks]):
                assert observation_equivalency_map is not None
                if type(observation_equivalency_map) is not circuitgym.spaces.ObservationMapping:
                    assert type(observation_equivalency_map) is list
                    assert all([type(item) is tuple for item in observation_equivalency_map])
                    self.observation_mapping = circuitgym.spaces.ObservationMapping(observation_equivalency_map)
                else:
                    self.observation_mapping = observation_equivalency_map
        else:
            observation_decks = [observation_decks]*nckts
            self.observation_mapping = circuitgym.spaces.ObservationMapping([(name,name) for name in observation_decks[0].keys()])

        self.circuit_args =[
            {
                'simfilename': filenames[i],
                'simdir': simdirs[i],
                'input_inventory': input_inventories[i],
                'observation_deck': observation_decks[i],
                'spectre_args': spectre_args,
                'spectre_source': spectre_source,
                'spectre_binary': spectre_binary,
                'spectre_env': spectre_env,
                'analysis_name': analysis_name,
                'sim_time_limit': sim_time_limit,
                'transient_time_res': transient_time_resolution,
                'logging': self.logging,
                'max_n_steps': self.max_n_steps,
                'cache_enabled': self.cache_enabled,
                'cache_level': self.cache_level,
                'multidiscrete2discrete': self.multidiscrete2discrete,
                'pyspectre_client': self.pyspectre_client,
                'replwrap_client': self.replwrap_client,
            } for i in range(self.ncircuits) ]

        self.circuits = [Circuit(defer_launch=True, **self.circuit_args[i]) for i in range(self.ncircuits)]

        # combined action space
        self.action_space = self.circuits[0].action_space

        if hasattr(self.action_space, 'nvec') and hasattr(self.action_space, 'n'):
            self.action_space.n = np.asscalar(np.product(self.action_space.nvec).astype(int))
        # else:
        #     self.action_space.n = np.Infinity

        # combine observation spaces
        #self.resolvetiepoints()
        self.observation_space = gym.spaces.Box(
            low=np.vstack([ckt.observation_space.low for ckt in self.circuits]).squeeze(1),
            high=np.vstack([ckt.observation_space.high for ckt in self.circuits]).squeeze(1),
            dtype=np.float16
        )

    def resolvetiepoints(self):
        obsset = list()
        for ckt in self.circuits:
            obsset.append(set(ckt.observation_deck.keys()))

        allobs = obsset[0]

        for item in obsset:
            allobs = allobs & item

        allobs = sorted(list(allobs))
        for ckt in self.circuits:
            ckt.observation_deck = circuitgym.ObservationDeck([ckt.observation_deck[item] for item in allobs])

            ckt.observation_space = gym.spaces.Box(
                np.dstack([obs.low for obs in ckt.observation_deck.values()]).squeeze(),
                np.dstack([obs.high for obs in ckt.observation_deck.values()]).squeeze(),
                dtype=np.float16
            )

    def launch_sims(self):
        [ckt.putlaunch() for ckt in self.circuits]
        [ckt.getlaunch() for ckt in self.circuits]
        self.launched = True

    def reset(self):
        if not self.launched:
            self.launch_sims()

        [ckt.putreset(block=False) for ckt in self.circuits]
        state = [ckt.getreset() for ckt in self.circuits]

        self.state = np.hstack(state)
        return self.state

    def step(self, action, return_waves=False):
        if not self.launched:
            self.launch_sims()

        # t0 = time.time()

        if type(action) is str and action == 'random':
            action = np.empty(shape=(0,))
            for inpt in self.input_inventories[0].values():
                if 'continuous' in inpt.action_mode:
                    if 'centered' in inpt.action_mode:
                        action = np.append(action, np.random.uniform(-1, 1, (1,)))
                    else:
                        action = np.append(action, np.random.uniform(0, 1, (1,)))
                elif 'integer' in inpt.action_mode or 'discrete' in inpt.action_mode:
                    action = np.append(action, np.random.randint(0, inpt.nlevels))
                else:
                    raise NotImplementedError('unsure how to take a random step for these kinds of inputs')

        action = np.array(action)
        states = len(self.circuits) * [None]
        time_vector = len(self.circuits) * [None]
        waves = len(self.circuits) * [None]
        done = len(self.circuits) * [None]
        info = len(self.circuits) * [None]

        """ do step """
        [ckt.putstep(action, block=False) for ckt in self.circuits]
        for ckt_no, ckt in enumerate(self.circuits):
            states[ckt_no], time_vector[ckt_no], waves[ckt_no], done[ckt_no], info[ckt_no] = ckt.getstep()

        """ do augmentation"""
        for ckt_no, ckt in enumerate(self.circuits):
            if self.augmentors[ckt_no]:
                waves[ckt_no] += np.sum(np.dstack(
                    [aug(ckt.state.reshape(1,-1), ckt.action2cktvalues(action).reshape(1,-1)) for aug in self.augmentors[ckt_no]]
                ),axis=2).reshape(waves[ckt_no].shape)

        """ if time vectors are equal (they should be), collapse them"""
        if np.all([time_vector[0] == vec for vec in time_vector]):
            time_vector = time_vector[0]
        else:
            time_vector = np.stack(time_vector, axis=0)

        newstate = np.hstack(states)
        waves = np.stack(waves,axis=0)
        reward = self.rewardfunction(self.state, waves, newstate)

        """ if you're logging, log the step """
        if hasattr(self, 'datablock'):
            self._logevent((
                self.state,
                np.hstack([ckt.action2cktvalues(action).ravel() for ckt in self.circuits]),
                waves,
                reward,
                newstate,
            ))

        """ prep return values and return """
        self.state = newstate
        info = {}
        # t1 = time.time()
        # print('stepped. ({}s)'.format(t1-t0))

        done = True if True in done else False
        if not return_waves:
            return self.state, reward, done, info
        else:
            return self.state, reward, done, info, (time_vector, waves)

    def render(self, mode='human', close=False):
        """Renders the environment.
        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.)

        # Arguments
            mode (str): The mode to render with.
            close (bool): Close all open renderings.
        """
        # if self.figure is None:
        #     self.figure, self.ax1 = plt.subplots()
        #     self.figuredata, = self.plotfunction()
        #     self.figure.canvas.draw()
        #     plt.show(block=False)
        #     sleep(1 / 50)
        #
        # self.plotfunction()
        # self.figure.canvas.draw()
        # sleep(1 / 50)
        return None

    def close(self):
        """Override in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        if self.circuits:
            for ckt in self.circuits:
                if ckt is not None:
                    ckt.close()
        return None

    def seed(self, seed=None):
        pass

    def _init_datalogging(self, datapath, filename, maxrows):
        global pd
        import pandas as pd

        if isinstance(datapath, str):
            self.datablock_path = datapath
        else:
            self.datablock_path = './circuitgym'

        if isinstance(filename, str):
            self.datablock_prefix = filename
        else:
            self.datablock_prefix = 'cglog'

        os.makedirs(self.datablock_path, exist_ok=True)
        self.datablock_columns = ['state','action','response','reward','nextstate']
        self.datablock_index = 0
        self.datablock = []
        self.datablock_max_size = maxrows

    def _logevent(self, event):
        assert len(event) == len(self.datablock_columns)
        ## append buffer
        self.datablock.append(event)

        ## if table is long enough, write it to disk and clear it
        if len(self.datablock) == self.datablock_max_size:
            self.flush_datablock()

    def flush_datablock(self, reset_index=False, use_multiindex=False):
        if self.datablock:
            assert len(self.datablock[0]) == len(self.datablock_columns)
            filename = '{}.{}.hd5'.format(self.datablock_prefix, self.datablock_index)
            _write_experience_file(self.datablock,
                                   self.datablock_path,
                                   filename,
                                   self.datablock_columns,
                                   self.ncircuits,
                                   use_multiindex=use_multiindex)
            self.datablock_index = self.datablock_index + 1 if not reset_index else 0
            self.datablock = []


class Circuit(gym.Env):
    """The abstract environment class that is used by all agents. This class has the exact
    same API that OpenAI Gym uses so that integrating with it is trivial. In contrast to the
    OpenAI Gym implementation, this class only defines the abstract methods without any actual
    implementation.
    """

    def signal_handler(self, signal, frame):
        if hasattr(self, 'internalsim'):
            if hasattr(self.internalsim, 'close'):
                self.close()
        raise KeyboardInterrupt

    def __init__(self,
                 simfilename='input.scs',
                 analysis_name='tran',
                 simdir=None,
                 spectre_args=None,
                 spectre_source=None,
                 spectre_binary='spectre',
                 spectre_env=None,
                 input_inventory=None,
                 observation_deck=None,
                 sim_time_limit=None,
                 max_n_steps=None,
                 transient_time_res=None,
                 logging=False,
                 savedatadir=None,
                 cache_enabled=False,
                 cache_level=4,
                 multidiscrete2discrete=False,
                 defer_launch=False,
                 pyspectre_client=False,
                 replwrap_client=False,
                 ):

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGABRT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        for item in input_inventory.values():
            assert issubclass(type(item), circuitgym.spaces.CircuitInput)

        for item in observation_deck.values():
            assert issubclass(type(item), circuitgym.spaces.CircuitObservation)

        assert sim_time_limit or max_n_steps
        if sim_time_limit:
            assert isinstance(sim_time_limit, float)
        if max_n_steps:
            assert isinstance(max_n_steps, (int, float))

        self.simfilename = simfilename
        self.analysis_name = analysis_name
        self.simdir = simdir
        self.spectre_args = spectre_args
        self.spectre_source = spectre_source
        self.logging = logging
        self.savedatadir = savedatadir
        self.input_inventory = input_inventory
        self.observation_deck = observation_deck
        self.sim_time_limit = sim_time_limit
        self.max_n_steps = max_n_steps
        self.simtime = 0.0
        self.nsteps = 0
        self.dcstate = None
        self.dcfile = None
        self.tranfile = None
        self.state = None
        self.cache_enabled=cache_enabled
        self.cache_level=cache_level
        self.cache_hitcount = 0
        self.cache_misscount = 0
        self.multidiscrete2discrete= multidiscrete2discrete
        self.replwrap_client = replwrap_client
        self.pyspectre_client = pyspectre_client
        self.launched=False


        if all(['continuous' in inpt.action_mode for inpt in self.input_inventory.values()]):
            if all(['centered' in inpt.action_mode for inpt in self.input_inventory.values()]):
                high = [1.0] * len(self.input_inventory)
                low = [-1.0] * len(self.input_inventory)
            elif not any(['centered' in inpt.action_mode for inpt in self.input_inventory.values()]):
                high = [1.0] * len(self.input_inventory)
                low = [0.0] * len(self.input_inventory)
            else:
                high = [inpt.high for inpt in self.input_inventory]
                low = [inpt.low for inpt in self.input_inventory]

            self.action_mode = 'continuous'
            self.action_space = gym.spaces.Box(
                low=np.array(low),
                high=np.array(high),
                dtype=np.float16)

        elif all(['discrete' in inpt.action_mode or 'integer' in inpt.action_mode for inpt in self.input_inventory.values()]):
            if self.multidiscrete2discrete:
                self.action_space = gym.spaces.Discrete(
                    int(np.product(np.array([inpt.action_space.n for inpt in self.input_inventory.values()]))))
            else:
                self.action_space = gym.spaces.MultiDiscrete(
                    np.array([inpt.action_space.n for inpt in input_inventory.values()]).astype(int)
                )

        else:
            raise NotImplementedError

        self.simtimestep = float(np.array([inpt.maxtimestep for inpt in self.input_inventory.values()]).min())

        if transient_time_res is not None:
            assert isinstance(transient_time_res, (float, int))
            self.trasient_time_res = transient_time_res
        else:
            self.trasient_time_res = np.divide(self.simtimestep,50.0,signature=(np.float32, np.float32, np.float32))

        if self.observation_deck is None or '*' in self.observation_deck:
            listofobservations = []
            allstates = self.get_state_list()
            for statename in allstates:
                listofobservations.append(
                    circuitgym.CircuitObservation(
                        netname=statename,
                        minval=np.asscalar(self.observation_deck['*'].low),
                        maxval=np.asscalar(self.observation_deck['*'].high)
                    )
                )
            self.observation_deck = circuitgym.ObservationDeck(listofobservations)

        self.observation_space = gym.spaces.Box(
            low=np.vstack([obs.low for obs in self.observation_deck.values()]).squeeze(axis=1),
            high=np.vstack([obs.high for obs in self.observation_deck.values()]).squeeze(axis=1),
            dtype=np.float16
        )

        """instantiate internal sim:"""
        pyspectre_args={
            'netlist': self.simfilename,
            'simdirectory': self.simdir,
            'analysis_name': self.analysis_name,
            'spectreargs': self.spectre_args,
            'sourcefile': spectre_source,
            'spectre_binary': spectre_binary,
            'spectre_env': spectre_env,
            'logging': self.logging,
            'replwrap_client': self.replwrap_client,
            'pyspectre_client': self.pyspectre_client,
        }

        if defer_launch:
            pyspectre_args.update({'delayed_start': True})

        self.internalsim = Pyspectre(**pyspectre_args)

        if not defer_launch:
            self.launch()

        if self.cache_enabled:
            self.cache={}
            self.trace=[]
            self.cache_hitcount=0
            self.cache_misscount=0

    def launch(self):
        self.putlaunch()
        self.getlaunch()

    def putlaunch(self):
        self.internalsim.startbinary(block=False)

    def getlaunch(self):
        self.internalsim.wait()
        self.internalsim.resolve_analysis_type()
        self.launched = True

    def reset(self):
        """
        Resets the state of the environment and returns an initial observation.

        # Returns
            observation (object): The initial observation of the space. Initial reward is assumed to be 0.
        """
        self.putreset(block=True)
        return self.getreset()

    def putreset(self, block=True):

        if not self.launched:
            self.launch()

        # reset simulation time
        self.simtime = 0.0
        self.nsteps = 0
        self.trace = []

        # while True:
        #     try:
                # reset all circuit inputs
        [inpt.reset(self, block=block) for inpt in self.input_inventory.values()]
        # self.set_spectre_values()

        if self.dcstate is None:
            self.internalsim.init(stepsize=self.simtimestep, block=True)

        self.internalsim.reset(sampleinterval=self.trasient_time_res, block=block)

    def getreset(self):

        self.internalsim.wait()

        if self.dcstate is None:
            allstates = self.internalsim.readdcfile()
            self.dcstate = np.array([allstates[obs] for obs in self.observation_deck.keys()])

        self.state = self.dcstate
        return self.state

    def step(self, action):
        """Run one timestep of the environment's dynamics.
        Accepts an action and returns a tuple (observation, reward, done, info).
        # Arguments
            action (object): An action provided by the environment.
        # Returns
            observation (object): Agent's observation of the current environment.
            reward (float) : Amount of reward returned after previous action.
            done (boolean): Whether the episode has ended, in which case further step() calls
            will return undefined results.
            info (dict): Contains auxiliary diagnostic information (helpful for debugging, and sometimes learning).
        """

        self.putstep(action)
        return self.getstep()

    def putstep(self,action, block=True):

        if not self.launched:
            self.launch()

        self.trace.append(action)
        if self.cache_enabled and len(self.trace) <= self.cache_level:
            t_id = hash(str(np.array(self.trace)))
            if t_id in self.cache:
                self.cache_hitcount += 1
                return
            else:
                self.cache_misscount += 1

        actions = self.decode_action(action)
        self.apply_actions(actions)
        stoptime = self.simtime + self.simtimestep
        self.internalsim.step(stepsize=self.simtimestep, resolution=self.trasient_time_res, block=block)
        self.simtime = stoptime
        self.nsteps += 1
        return False

    def getstep(self):
        if self.cache_enabled and len(self.trace) <= self.cache_level:
            t_id = hash(str(np.array(self.trace)))
            if t_id in self.cache:
                return self.cache[t_id]

        self.internalsim.wait()
        states = self.internalsim.readtranfile()
        times, waves = self.internalsim.get_data([obs.cname for obs in self.observation_deck.values()])

        self.state = np.array([states[obsname] for obsname in self.observation_deck.keys()])

        if self.sim_time_limit and self.simtime >= self.sim_time_limit:
            done = True
        elif self.max_n_steps and self.nsteps >= self.max_n_steps:
            done = True
        else:
            done = False

        info = {}
        result = self.state, times, waves, done, info

        if self.cache_enabled and len(self.trace) <= self.cache_level:
            t_id = hash(str(np.array(self.trace)))
            self.cache.update({t_id: result})

        return result

    def get_state_list(self):
        """
        Runs a DC simulation to get a list of all observable states

        # Returns
            observation (object): The initial observation of the space. Initial reward is assumed to be 0.
        """
        if not self.launched:
            self.launch()

        # reset all circuit inputs
        for inpt in self.input_inventory.values():
            inpt.current_level = inpt.initial_level
            inpt.current_value = inpt.level2value(inpt.current_level)
            inpt.set_spectre_values(self)

        # reset simulation time
        self.simtime = 0.0
        self.nsteps = 0

        if self.dcstate is None:
            self.dcfile = self.internalsim.rundc()
        data = self.internalsim.readdcfile()

        return sorted(list(data.keys()))

    def decode_action(self, action):
        action = np.array(action) ## cast it
        if action.size == len(self.input_inventory):
            return action
        else:
            n_levels = [inpt.nlevels for inpt in self.input_inventory.values()]
            n_digits = [len(np.binary_repr(n-1)) for n in n_levels]
            t_digits = np.sum(n_digits)
            b = np.binary_repr(action).zfill(np.asscalar(t_digits.astype(int)))
            cum_digits = np.cumsum(n_digits)
            starts = cum_digits-n_digits
            stops = cum_digits
            choice = [np.array(list(b[starts[ind]:stops[ind]])).astype(int) for ind in range(len(starts))]
            choice = [np.dot(x, 1 << np.arange(x.size)[::-1]) for x in choice]
            return np.array(choice)

    def apply_actions(self, decoded_actions):

        if not self.launched:
            self.launch()

        assert decoded_actions.size == len(self.input_inventory)
        for inputno, ckinpt in enumerate(self.input_inventory.values()):
            ckinpt.take_action(decoded_actions[inputno], self)
            #ckinpt.set_spectre_values(self)

    def action2cktvalues(self, action):
        decoded_actions = self.decode_action(action)
        return np.array([inpt.level2value(inpt.action2level(decoded_actions[i])) for i,inpt in enumerate(self.input_inventory.values())])

    # def set_spectre_values(self):
    #     for item in self.input_inventory.values():
    #         item.set_spectre_values(self)

    def render(self, mode='human', close=False):
        """Renders the environment.
        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.)

        # Arguments
            mode (str): The mode to render with.
            close (bool): Close all open renderings.
        """
        raise NotImplementedError()

    def close(self):
        """Override in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        if hasattr(self, 'internalsim') and self.internalsim is not None:
            if self.logging and hasattr(self, 'resultsdir') and os.path.isdir(self.internalsim.resultsdir):
                shutil.copytree(
                    self.internalsim.resultsdir,
                    self.savedatadir + '/' + self.internalsim.resultsdir.split('/')[-1]
                )
            self.internalsim.cleanup()

    def seed(self, seed=None):
        """Override in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        raise NotImplementedError()



class WrappedCircuit(Circuit):
    def __init__(self, circuit):
        self=circuit
        self.parallelComp=[]
        self.serialComp=[]
