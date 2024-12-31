from kivy.factory import Factory

# Alias for the register function from Factory
register = Factory.register

"""
Registers custom components to the Kivy Factory.

This code registers each component within the "components" directory to the Kivy Factory. 
Once registered, the components can be used without explicitly importing them elsewhere in the kvlang files.
"""

# Register the component with Kivy's Factory
register("Container", module="kvdeveloper.components.Container")
register("ITDCard", module="kvdeveloper.components.ITDCard")
register("ResponsiveGrid", module="kvdeveloper.components.ResponsiveGrid")
register("LazyManager", module="kvdeveloper.components.LazyManager")
register("LoadingLayout", module="kvdeveloper.components.LoadingLayout")
