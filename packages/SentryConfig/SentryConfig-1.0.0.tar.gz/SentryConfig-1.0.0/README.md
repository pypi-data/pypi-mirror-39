# sentry-config: An application ini parsing solution
I originally was using this in [Crow-IRCServer](https://github.com/AWilliams17/PasteMate), but I've been wanting to use it
in some other things so I figured I'd go ahead and yank it out and make it it's own package and throw it up on PyPi.
What this essentially does is make it extremely easy to load and save .ini files. With validation. I'll demonstrate.

## Usage
### Set up
You define the structure of the ini file to be saved/loaded as such:
```python
from sentry-config.config import SentryConfig, SentryOption
from sentry-config.validators import IntRequired

class ExampleConfig(SentryConfig):  # ExampleConfig essentially acts as a representation of the external .ini file.
    class ExampleSection:  # This will translate to [ExampleSection] in the .ini,
        OptionOne = SentryOption(  # This will translate to optionone in the .ini
            default=1,
            criteria=IntRequired,
            description="This will translate to 'optionone' in the .ini file"
		)

        OptionTwo = SentryOption(
            default="Hello world",
            criteria=None,
            description="This translates to 'optiontwo' in the .ini file"
        )
```
And then, flush the config to produce the .ini (first check to make sure it doesn't already exist.)  
Flush config takes the current values of the SentryConfig instance's members and then flushes them out to a .ini
```python
# ...
ini_path = getcwd() + "/example.ini"

config_container = ExampleConfig(ini_path)

if not path.exists(ini_path):
    config_container.flush_config()
```
Since the .ini in this case didn't exist yet, it will use default values.  
The .ini which is produced is as follows:
```ini
[ExampleSection]
optionone = 1
optiontwo = Hello world
```
You can then read values from this .ini which will automatically set the option properties in the config container:
```python
config_container.read_config
print(config_container.ExampleSection.OptionOne)  # Prints 1
```
Options which get loaded from a .ini will automatically be parsed and converted to their appropriate types as specified in the  
sentry option criteria argument. EG: IntRequired parses 'optionone' into an int, before it is used as the value of OptionOne.

## Criteria
Sentry uses criteria when validating and converting values from an ini file.  
Criteria is optional (just pass 'None' to the criteria argument)
```python
from sentry_config.criteria import SentryCriteria


class MustBeOne(SentryCriteria):
    def criteria(self, value):
        if value != 1:
            return "I must be equal to one!"  # The return value here is used in the CriteriaNotMet exception.
```
And back in the ExampleConfig class defined earlier,
```python
class ExampleSection:
        OptionOne = SentryOption(
            default=1,
            criteria=[IntRequired, MustBeOne],
            description="This will translate to 'optionone' in the .ini file - It must be equal to '1'."
        )
```
Upon loading an ini, the value will be first converted into an int, and then it will run through any further criteria.  
If at any point a criteria check fails, a CriteriaNotMet exception will be raised with appropriate information as to which option  
failed to validate.

## Further examples
I've included an example right in the repo, check out the 'example' directory.  

## Caveats
With the way this is all set up, you unfortunately can not have a .ini file without a section for options to reside under.  
EG:
```python
class ExampleConfig(SentryConfig):
        OptionOne = SentryOption(
            default=1,
            criteria=IntRequired,
            description="This will translate to 'optionone' in the .ini file"
        )
```
Will just not work. It produces a blank .ini. I'll eventually look into fixing that.

## Contributing  
I don't really have any qualms what so ever about someone working on this since I probably won't get much done on it, as it  
works fine as is. If you wish to make pull requests, feel free. Just follow what the overall structure and style in the code  
is though.

## License
On that note, this is licensed under the GNU General Public License, so feel free to do whatever you want the code.
