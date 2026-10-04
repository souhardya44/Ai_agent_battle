from experiment import run_battle, run_depth_experiment, save_battle, save_depth


def main():
    battle = run_battle(10)
    depth = run_depth_experiment()

    save_battle(battle, "results/results.csv")
    save_depth(depth, "results/depth_experiment.csv")

    print("AI Agent Battle complete.")
    print("Saved: results/results.csv")
    print("Saved: results/depth_experiment.csv")


if __name__ == "__main__":
    main()
