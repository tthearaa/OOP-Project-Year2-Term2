def _banner():
    print("\n" + "═" * 52)
    print("   👗  CLOTHING INVENTORY & SALES SYSTEM  👗")
    print("═" * 52)

def _section(title):
    print(f"\n  ── {title} {'─' * max(0, 38 - len(title))}")

def _pause():
    input("\n  [Press Enter to continue]")