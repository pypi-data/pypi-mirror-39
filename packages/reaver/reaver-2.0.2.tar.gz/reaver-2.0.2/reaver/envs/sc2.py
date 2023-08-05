import gin
import numpy as np
from pysc2.lib import actions
from pysc2.lib import features
from pysc2.lib import protocol
from pysc2.env.environment import StepType
from . import Env, Spec, Space


@gin.configurable
class SC2Env(Env):
    def __init__(
        self,
        map_name='MoveToBeacon',
        render=False,
        reset_done=True,
        max_ep_len=None,
        spatial_dim=16,
        step_mul=8,
        obs_features=None,
        action_ids=None
    ):
        super().__init__(map_name, render, reset_done, max_ep_len)

        self.step_mul = step_mul
        self.spatial_dim = spatial_dim
        self._env = None

        if not action_ids:
            # Sensible defaults for all minigames
            action_ids = [0, 1, 2, 3, 4, 6, 7, 12, 13, 140, 168, 261, 274, 331, 332, 333, 334, 451, 452, 453]

        self.act_wrapper = ActionWrapper(spatial_dim, action_ids)
        self.obs_wrapper = ObservationWrapper(obs_features, action_ids)

    def start(self):
        # importing here to lazy-load
        from pysc2.env import sc2_env

        self._env = sc2_env.SC2Env(
            map_name=self.id,
            visualize=self.render,
            agent_interface_format=[features.parse_agent_interface_format(
                feature_screen=self.spatial_dim,
                feature_minimap=self.spatial_dim,
                rgb_screen=None,
                rgb_minimap=None
            )],
            step_mul=self.step_mul,)

    def step(self, action):
        try:
            obs, reward, done = self.obs_wrapper(self._env.step(self.act_wrapper(action)))
        except protocol.ConnectionError:
            # hacky fix from websocket timeout issue...
            # this results in faulty reward signals, but I guess it beats completely crashing...
            self.restart()
            return self.reset(), 0, 1

        if done and self.reset_done:
            obs = self.reset()

        return obs, reward, done

    def reset(self):
        try:
            obs, reward, done = self.obs_wrapper(self._env.reset())
        except protocol.ConnectionError:
            # hacky fix from websocket timeout issue...
            # this results in faulty reward signals, but I guess it beats completely crashing...
            self.restart()
            return self.reset()

        return obs

    def stop(self):
        self._env.close()

    def restart(self):
        self.stop()
        self.start()

    def obs_spec(self):
        if not self.obs_wrapper.spec:
            self.make_specs()
        return self.obs_wrapper.spec

    def act_spec(self):
        if not self.act_wrapper.spec:
            self.make_specs()
        return self.act_wrapper.spec

    def make_specs(self):
        # importing here to lazy-load
        from pysc2.env import mock_sc2_env
        mock_env = mock_sc2_env.SC2TestEnv(map_name=self.id, agent_interface_format=[
            features.parse_agent_interface_format(feature_screen=self.spatial_dim, feature_minimap=self.spatial_dim)])
        self.act_wrapper.make_spec(mock_env.action_spec())
        self.obs_wrapper.make_spec(mock_env.observation_spec())
        mock_env.close()


class ObservationWrapper:
    def __init__(self, _features=None, action_ids=None):
        self.spec = None
        if not _features:
            # available actions should always be present and in first position
            _features = {
                'screen': ['player_id', 'player_relative', 'selected', 'unit_hit_points', 'unit_hit_points_ratio',
                           'unit_density', 'unit_density_aa'],
                'minimap': ['player_id', 'player_relative', 'selected'],
                'non-spatial': ['available_actions', 'player']}
        self.features = _features
        self.feature_masks = {
            'screen': [i for i, f in enumerate(features.SCREEN_FEATURES._fields) if f in _features['screen']],
            'minimap': [i for i, f in enumerate(features.MINIMAP_FEATURES._fields) if f in _features['minimap']],}
        self.action_ids = action_ids

    def __call__(self, timestep):
        ts = timestep[0]
        obs, reward, done = ts.observation, ts.reward, ts.step_type == StepType.LAST

        obs_wrapped = [
            obs['feature_screen'][self.feature_masks['screen']],
            obs['feature_minimap'][self.feature_masks['minimap']]
        ]
        for feat_name in self.features['non-spatial']:
            if feat_name == 'available_actions':
                fn_ids_idxs = [i for i, fn_id in enumerate(self.action_ids) if fn_id in obs[feat_name]]
                mask = np.zeros((len(self.action_ids),), dtype=np.int32)
                mask[fn_ids_idxs] = 1
                obs[feat_name] = mask
            obs_wrapped.append(obs[feat_name])

        return obs_wrapped, reward, done

    def make_spec(self, spec):
        spec = spec[0]

        default_dims = {
            'available_actions': (len(self.action_ids), ),
        }

        screen_shape = (len(self.features['screen']), *spec['feature_screen'][1:])
        minimap_shape = (len(self.features['minimap']), *spec['feature_minimap'][1:])
        screen_dims = get_spatial_dims(self.features['screen'], features.SCREEN_FEATURES)
        minimap_dims = get_spatial_dims(self.features['minimap'], features.MINIMAP_FEATURES)

        spaces = [
            SC2Space(screen_shape, 'screen', self.features['screen'], screen_dims),
            SC2Space(minimap_shape, 'minimap', self.features['minimap'], minimap_dims),
        ]

        for feat in self.features['non-spatial']:
            if 0 in spec[feat]:
                spec[feat] = default_dims[feat]
            spaces.append(Space(spec[feat], name=feat))

        self.spec = Spec(spaces, 'Observation')


class ActionWrapper:
    def __init__(self, spatial_dim, action_ids, args=None):
        self.spec = None
        if not args:
            args = [
                'screen',
                'minimap',
                'screen2',
                'queued',
                'control_group_act',
                'control_group_id',
                'select_add',
                'select_point_act',
                # 'select_unit_act',
                # 'select_unit_id'
                'select_worker',
                # 'build_queue_id',
                # 'unload_id'
            ]
        self.func_ids = action_ids
        self.args, self.spatial_dim = args, spatial_dim

    def __call__(self, action):
        defaults = {
            'control_group_act': 0,
            'control_group_id': 0,
            'select_point_act': 0,
            'select_unit_act': 0,
            'select_unit_id': 0,
            'build_queue_id': 0,
            'unload_id': 0,
        }
        fn_id_idx, args = action.pop(0), []
        fn_id = self.func_ids[fn_id_idx]
        for arg_type in actions.FUNCTIONS[fn_id].args:
            arg_name = arg_type.name
            if arg_name in self.args:
                arg = action[self.args.index(arg_name)]
                # pysc2 expects all args in their separate lists
                if type(arg) not in [list, tuple]:
                    arg = [arg]
                # pysc2 expects spatial coords, but we have flattened => attempt to fix
                if len(arg_type.sizes) > 1 and len(arg) == 1:
                    arg = [arg[0] % self.spatial_dim, arg[0] // self.spatial_dim]
                args.append(arg)
            else:
                args.append([defaults[arg_name]])

        return [actions.FunctionCall(fn_id, args)]

    def make_spec(self, spec):
        spec = spec[0]

        spaces = [SC2FuncIdSpace(self.func_ids, self.args)]
        for arg_name in self.args:
            arg = getattr(spec.types, arg_name)
            if len(arg.sizes) > 1:
                spaces.append(Space(domain=(0, arg.sizes), categorical=True, name=arg_name))
            else:
                spaces.append(Space(domain=(0, arg.sizes[0]), categorical=True, name=arg_name))

        self.spec = Spec(spaces, "Action")


class SC2Space(Space):
    def __init__(self, shape, name, spatial_feats=None, spatial_dims=None):
        if spatial_feats:
            name += "{%s}" % ", ".join(spatial_feats)
        self.spatial_feats, self.spatial_dims = spatial_feats, spatial_dims

        super().__init__(shape, name=name)


class SC2FuncIdSpace(Space):
    def __init__(self, func_ids, args):
        super().__init__(domain=(0, len(func_ids)), categorical=True, name="function_id")
        self.args_mask = []
        for fn_id in func_ids:
            fn_id_args = [arg_type.name for arg_type in actions.FUNCTIONS[fn_id].args]
            self.args_mask.append([arg in fn_id_args for arg in args])


def get_spatial_dims(feat_names, feats):
    feats_dims = []
    for feat_name in feat_names:
        feat = getattr(feats, feat_name)
        feats_dims.append(1)
        if feat.type == features.FeatureType.CATEGORICAL:
            feats_dims[-1] = feat.scale
    return feats_dims
