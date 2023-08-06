from .envs import Circuit

class CircuitProcessClient(Circuit):
    def __init__(self, circuit_args):
        self.inq = mp.Queue()
        self.outq = mp.Queue()
        self.server = mp.Process(target=CircuitProcessServer, args=(self.inq, self.outq, circuit_args))
        self.server.start()

    def init(self):
        self.action_space = self._get_action_space()
        self.observation_space = self._get_observation_space()

    def step(self, action):
        self.inq.put(('step',action))
        return self._checkandreturn('could not step child circuit')

    def putstep(self, action):
        self.inq.put(('step', action))
        return None

    def reset(self):
        self.inq.put('reset')
        return self._checkandreturn('could not reset child circuit')

    def putreset(self):
        self.inq.put('reset')

    def close(self):
        self.inq.put('kill')
        self.inq.put('STOP')
        return None

    def getresult(self):
        return self._checkandreturn('could not get result')

    def _get_action_space(self):
        self.inq.put('getactionspace')
        return self._checkandreturn('could not get child circuit action_space')

    def _get_observation_space(self):
        self.inq.put('getobservationspace')
        return self._checkandreturn('could not get child circuit observation_space')

    def _pingandblock(self):
        self.inq.put('hello')
        while self.outq.get() != 'world':
            sleep(0.5)
        return None

    def _checkandreturn(self, message):
        result = self.outq.get()
        if isinstance(result, str) and result == 'ERROR':
            raise RuntimeError(message)
        else:
            return result


def CircuitProcessServer(inq, outq, circuit_args):
    assert isinstance(inq, mp.queues.Queue)
    assert isinstance(outq, mp.queues.Queue)

    mycircuit = Circuit(launch=True, **circuit_args)

    try:
        for command in iter(inq.get, 'STOP'):
            if isinstance(command, tuple):
                fn = command[0]
                args = command[1:]
            elif isinstance(command, str):
                fn = command

            if fn == 'reset':
                try:
                    outq.put(mycircuit.reset())
                except:
                    outq.put('ERROR')

            elif fn =='step':
                try:
                    outq.put(mycircuit.step(*args))
                except:
                    outq.put('ERROR')

            elif fn == 'getactionspace':
                try:
                    outq.put(mycircuit.action_space)
                except:
                    outq.put('ERROR')

            elif fn == 'getobservationspace':
                try:
                    outq.put(mycircuit.observation_space)
                except:
                    outq.put('ERROR')

            elif fn == 'hello':
                try:
                    outq.put('world')
                except:
                    outq.put('ERROR')

            elif fn == 'kill':
                try:
                    outq.put(mycircuit.close())
                except:
                    outq.put('ERROR')

            else:
                outq.put('UNRECOGNIZED')

    except KeyboardInterrupt:
        mycircuit.close()
        raise KeyboardInterrupt