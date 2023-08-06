# Other imports.
from simple_rl.agents import RandomAgent, FixedPolicyAgent
from simple_rl.planning import ValueIteration
from simple_rl.tasks import GridWorldMDP, CartPoleMDP
from simple_rl.run_experiments import run_agents_on_mdp

def main():
	# Setup MDP.
	# mdp = GridWorldMDP(width=10, height=3, init_loc=(1, 1), goal_locs=[(10, 3)], gamma=0.95)

	mdp = CartPoleMDP()
	
	# vi = ValueIteration(mdp)
	# vi.run_vi()

	# Make agents.
	rand_agent = RandomAgent(actions=mdp.get_actions())
	# optimal_agent = FixedPolicyAgent(vi.policy)

	# Run experiment and make plot.
	run_agents_on_mdp([rand_agent], mdp, instances=3, episodes=500, steps=50)

if __name__ == "__main__":
	main()
