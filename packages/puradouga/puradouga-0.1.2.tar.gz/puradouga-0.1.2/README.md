# Puradouga

## Overview

Puradouga is the plugin system of uradouga. Currently its only task is to act as an interface between uradouga and metadouga. But it could also interact with other projects without problems, as long as they follow the corresponding guidelines.
Puradouga contains a generic plugin system which is defined within puradouga.core. Based on this, puradouga.plugins.media contains several classes, which serve as the base for the individual plugins. In addition, puradouga.plugins.data contains various data classes, which act as parameters for the plugins as well as results. The individual interfaces explicitly specify one of these data types or use a python data type.

## Usage

### Plugin

Puradouga uses dynamic loading of its plugins, so it is sufficient, if the plugins are located within a certain folder. This folder is provided by uradouga.

Puradouga initially searches for the implementations of its interfaces. To find them, they must be available through `import <pluginName>`.
This can be achieved by designing the plugin as a single file in which the implementations can be found. Alternatively, the plugin can be a package in which the implementations are imported into the \_\_init\_\_.py file.

Please note that puradouga must first execute the plugins normally in order to load them. It is therefore recommended not to have any code directly in the files, but all of them only accessible via the classes.

The process to create a plugin is relatively simple. First you have to find an appropriate interface. Then you write your own class based on it, which shows the desired behavior.

```python
from puradouga.plugins.media import TvMetaProvider
from puradouga.plugins import data as pm

class HelloWorld(TvMetaProvider):
    def series_from_filename(self, filename_parsed: pm.FilenameParsed) -> pm.SeriesResponse:
        return pm.SeriesResponse(title=pm.Title(english="Hello World"))
```

In the example above a series is parsed. The method gets an object as parameter, with different information about the file. Now we create an answer and set the title to `Hello World`. If uradouga would call this plugin, the series would all have a title of `Hello World`.

### Loader

To load plugins puradouga core is used mainly. The first step is to create a plugin system. This manages the individual plugins and provides methods for loading plugins. It is normally sufficient to use one PluginSystem within a project, but several can be used at the same time.
Next, the base classes of the plugins and the folders in which the plugins are located must be registered on this system. When the system is reloaded, it is ready to use.

```python
from puradouga.core import PluginSystem
from puradouga.plugins.media import TvMetaProvider

system = PluginSystem(auto_reload=False)
system.register_source("./plugins")  # Plugin folder
system.register_base_class(TvMetaProvider)  # Plugin base class
system.reload()
```

The next step is to create a filter. This will only return those plguins which correspond to a certain base class. All others will be ignored.
With the result different methods can be executed. These correspond to different strategies to execute the plugins. Depending on the method, you can sprint time because not all plugins have to be executed.

```python
from puradouga.core import PluginSystem
from test_puradouga.test_plugin_spec import MathPlugin

plugin_system = PluginSystem(auto_reload=False)
plugin_system.register_source("./plugins")
plugin_system.register_base_class(MathPlugin)
plugin_system.reload()

math_filter = plugin_system.get_filter(MathPlugin)

# Execute all plugins and return ordered by score
math_filter.eval_score(MathPlugin.operation, args=[27, 13])

# Execute all plugins one after another, until the code exits
results = list(math_filter.eval_ordered(MathPlugin.operation,
                                        lambda a: a,
                                        max_results=3,
                                        plugin_name_order=['Multiply', 'Divide', 'Subtract', 'Add'],
                                        args=[7, 5]))

``` 

Since the eval methods all work with yield, in the second example the code can abort after each item and does not have to execute all plugins. This is not possible in the first example, because this is sorted. All plugins must have already been evaluated.
Puradouga will filter incorrect answers as long as it is not in debug mode.
