import numpy as np
import gym
from gym import spaces

try:
    import lutorpy as lua
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: you need to install lutorpy, xitari and alewrap'.)".format(e))



class XitariEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}
    reward_range = (-np.inf, np.inf)
    
    @staticmethod
    def xitariScreenToNpRGB(screen):
        npArray = screen.asNumpyArray()[0]

        rgbArray = np.zeros((210,160,3), 'uint8')

        rgbArray[..., 0] = npArray[0]*256
        rgbArray[..., 1] = npArray[1]*256
        rgbArray[..., 2] = npArray[2]*256

        return rgbArray
    
    def __init__(self, game="space_invaders"):
        # require cutorch needed to enable gpu support
        # for ale environment
        # ?? do we need it, could prevent tensorflow from
        #    getting gpu resources
        # require("cutorch")
        
        # load lua alewrap framework
        framework = require("alewrap")
        
        # get option lua table for
        # alewrap
        opt_lua_table_str = """
        {
          -- game_path points to roms that came with OpenAIGym
          game_path = "/usr/local/lib/python2.7/dist-packages/atari_py/atari_roms",
          verbose = 2,
          actrep = 4,
          random_starts = 30,
          pool_frms = {
            type = "max",
            size = 2
          },
          -- -1 don't use; 0 use 0th
          gpu = -1,
          env = "%s",
          env_params = {
            useRGB = true
          }
        }
        """ % game
        self.opt = lua.eval(opt_lua_table_str)
        
        # load xitari game environment with the provided options
        self.gameEnv = framework.GameEnvironment(self.opt)
        
        
        # get valid game actions
        # to pass self prepend "_" before function name
        # see https://github.com/imodpasteur/lutorpy#prepending-self-as-the-first-argument-automatically
        self.gameActions = [action for action in self.gameEnv._getActions().values()]
        
        # setup action and observation spaces
        # to conform to OpenAI Gym protocol
        self.action_space = gym.spaces.Discrete(len(self.gameActions))
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(210, 160, 3))
        
        
    def _reset(self, full_reset=True):
        """
        Resets the state of the environment and returns an initial observation.
        Outputs
        -------
        observation (object): the initial observation of the space. (Initial reward is assumed to be 0.)
        """
        # taken from https://github.com/kuz/DeepMind-Atari-Deep-Q-Learner/blob/master/dqn/train_agent.lua#L86
        if self.opt.random_starts > 0:
            screen, reward, terminal = self.gameEnv._nextRandomGame()
        else:
            screen, reward, terminal = self.gameEnv._newGame()
        
        if full_reset and self.gameEnv["_state"]["lives"] is not 3:
            print 'WARNING: Xitari game lives count (%s) is not 3; repeating reset' % self.gameEnv["_state"]["lives"]
            return self._reset(full_reset=full_reset)
        
        self.isDone = terminal
        self.latestSate = self.xitariScreenToNpRGB(screen)
        return self.latestSate
    
    
    def _step(self, action_id):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Input
        -----
        action : an action provided by the environment
        Outputs
        -------
        (observation, reward, done, info)
        observation (object): agent's observation of the current environment
        reward (float) : amount of reward due to the previous action
        done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
        info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        isTraining = True
        screen, reward, terminal = self.gameEnv.step(self.gameEnv, self.gameActions[action_id], isTraining)

        self.isDone = terminal
        self.latestSate = self.xitariScreenToNpRGB(screen)

        return self.latestSate, reward, self.isDone, {}
    

    
    def _render(self, mode='human', close=False):
        """Renders the environment.
        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) By convention,
        if mode is:
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).
        Note:
            Make sure that your class's metadata 'render.modes' key includes
              the list of supported modes. It's recommended to call super()
              in implementations to use the functionality of this method.
        Args:
            mode (str): the mode to render with
            close (bool): close all open renderings"""
        
        img = np.copy(self.latestSate)
        
        if mode is 'rgb_array':
            return img # return RGB frame suitable for video
        elif mode is 'human':
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
        else:
            super(XitariENV, self).render(mode=mode) # raise an exception
