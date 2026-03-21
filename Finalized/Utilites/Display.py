#Header for the menu
def _banner():
    print("\n" + "═" * 52)
    print("  ARV Studios INVENTORY & SALES SYSTEM  ")
    print("═" * 52)

def _section(title):
    print(f"\n  {'─' * max(0, 38 - len(title))} {title} {'─' * max(0, 38 - len(title))}")

def _pause(): #shift user's attention to the current problem
    input("\n  [Press Enter to continue]")

if __name__ == "__main__":
    _banner()
    _section("Hello")
    _pause()
    _section("Pneumonou")