from gym.envs import register

register(
    id='nevolution-risk-v0',
    entry_point='nevolution_risk.env:RiskEnv',
)