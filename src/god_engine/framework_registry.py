"""
Ethical and directive framework loader.
"""

class FrameworkRegistry:
    def __init__(self, config):
        self.config = config
        self.directive = self.config.get("directives", {}).get("core_directive")
        self.ethical_framework = self.config.get("directives", {}).get("ethical_framework")
        self._load_frameworks()

    def _load_frameworks(self):
        """Loads the specified ethical and directive frameworks."""
        print(f"Loading directive: {self.directive}")
        print(f"Loading ethical framework: {self.ethical_framework}")
        # Placeholder for actual framework loading logic
        pass

    def get_directive(self):
        return self.directive
