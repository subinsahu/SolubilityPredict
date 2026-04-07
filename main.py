"""
Entry point for the solubility prediction project.

Usage:
  python main.py train                          # train the model
  python main.py predict "CCO"                  # predict a single SMILES
  python main.py predict "CCO" "c1ccccc1" "CC"  # predict multiple SMILES
"""

import sys


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "train":
        from src.train import train
        train()

    elif command == "predict":
        if len(sys.argv) < 3:
            print("Provide at least one SMILES string.\nExample: python main.py predict CCO")
            sys.exit(1)

        import os
        if not os.path.exists("data/model.pkl"):
            print("No trained model found. Run: python main.py train")
            sys.exit(1)

        from src.predict import predict
        smiles_list = sys.argv[2:]
        results = predict(smiles_list)

        print(f"\n{'SMILES':<40} {'logS':>8} {'Solubility':>12}  Category")
        print("-" * 80)
        for r in results:
            if r["error"]:
                print(f"{r['smiles']:<40}  ERROR: {r['error']}")
            else:
                print(
                    f"{r['smiles']:<40} {r['logS']:>8.3f} {r['solubility_mol_L']:>12}  {r['category']}"
                )

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
