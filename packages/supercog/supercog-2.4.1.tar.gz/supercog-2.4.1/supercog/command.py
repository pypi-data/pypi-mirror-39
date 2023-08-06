"""
This is a file that contains 4 classes used to create a Command for a Discord Bot.

An Error object simply holds a list of possible error messages that can be chosen at random.

An AcceptedParameter object simply holds any alternatives a parameter can follow and what that
specific parameter is.

A Parameter object holds the information about what the parameter signifies and whether or not it is
optional. Optionally, you can add a dictionary of AcceptedParameter objects to it in order to be able
to be more specific about a Parameter.

A Command object contains a multitude of options for a Command in a Discord Bot:
    * Alternative names
    * Whether or not it's NSFW
    * Whether or not only Server Moderators can run it
    * Whether or not only Bot Moderators can run it
    * The Parameters for the Command
    * The Errors for the Command
    * A custom Command function
        Note: This is useful especially when every Command's function inside a Category
              follows the same parameter format. It allows you to loop over each command and
              handle the logic inside the proper function.

The Markdown function will automatically generate Markdown text to layout the contents of
the Command you call it on. Each Command will be given the following format:

    Alternatives | Parameters | Any tags (NSFW, Server Mod, Bot Mod) | Command Information
    Accepted Parameters for each Parameter
        Parameter Alternatives | Parameter Information

The HTML function will follow the same format but it generates HTML code instead.
"""

from .exception import EmptyAcceptedParameterException, EmptyCommandException, EmptyErrorException, EmptyParameterException
from .exception import NoSuchAcceptedParameterException, NoSuchErrorException, NoSuchParameterException
from .exception import MissingTextFormatException

from .censor import censor

from random import choice

class Error:
    """Creates a new Error object.
    There are two (2) different ways to make an `Error` object:
        1.) Clarify the messages parameter in the constructor.
        2.) Clarify a dictionary that holds the messages for the error.
    
    You must do one or the other. 
    If they are both missing, an `EmptyErrorException` will occur.
    If both are included, the `messages` parameter will be used.

    If the `errorDict` parameter is used, the following tags must be included:
        \"messages\"

    Parameters:
        messages (list): The messages this Error object holds. (Defaults to None)
        errorDict (dict): The dict that holds the messages for this Error. (Defaults to None)
    """
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Constructor
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def __init__(self, *, messages = None, errorDict = None):
        """Creates a new Error object.
        There are two (2) different ways to make an `Error` object:
            1.) Clarify the messages parameter in the constructor.
            2.) Clarify a dictionary that holds the messages for the error.
        
        You must do one or the other. 
        If they are both missing, an `EmptyErrorException` will occur.
        If both are included, the `messages` parameter will be used.

        If the `errorDict` parameter is used, the following tags must be included:
            \"messages\"

        Parameters:
            messages (list): The messages this Error object holds. (Defaults to None)
            errorDict (dict): The dict that holds the messages for this Error. (Defaults to None)
        """

        # Check if messages and errorDict are both None
        if messages == None and errorDict == None:
            raise EmptyErrorException("You must include the messages parameter or errorDict parameter.")
        
        # messages parameter exists
        if messages != None:
            self._messages = messages
        
        # errorDict parameter exists
        elif errorDict != None:
            self._messages = errorDict["messages"]
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def getMessages(self):
        """Returns the messages that this `Error` object holds.
        """

        return self._messages
    
    def getMessage(self):
        """Returns a random error message for this `Error`
        """

        return choice(self._messages)

class AcceptedParameter:
    """Creates a new AcceptedParameter object.
    There are two (2) different ways to make an `AcceptedParameter` object:
        1.) Clarify the alternatives and info parameters in the constructor.
        2.) Clarify a dictionary that holds the alternative names and info for the parameter.
    
    You must do one or the other.
    If they are both missing, an `EmptyAcceptedParameterException` will occur.
    If both are included, the `alternatives` and `info` parameters will be used.

    If the `acceptedParameterDict` parameter is used, the following tags must be included:
        \"alternatives\"
        \"info\"
            Note: For the \"info\" tag, you can also give it a dictionary for dynamic hyperlinking. (Default is no hyperlink)
    Parameters:
        alternatives (list): The alternative names that can be used for this accepted parameter.
        info (str): The description of this accepted parameter.
    """

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Constructor
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def __init__(self, *, alternatives = None, info = None, acceptedParameterDict = None):
        """Creates a new AcceptedParameter object.
        There are two (2) different ways to make an `AcceptedParameter` object:
            1.) Clarify the alternatives and info parameters in the constructor.
            2.) Clarify a dictionary that holds the alternative names and info for the parameter.
        
        You must do one or the other.
        If they are both missing, an `EmptyAcceptedParameterException` will occur.
        If both are included, the `alternatives` and `info` parameters will be used.

        If the `acceptedParameterDict` parameter is used, the following tags must be included:
            \"alternatives\"
            \"info\"
                Note: For the \"info\" tag, you can also give it a dictionary for dynamic hyperlinking. (Default is no hyperlink)
        Parameters:
            alternatives (list): The alternative names that can be used for this accepted parameter.
            info (str): The description of this accepted parameter.
        """

        # Check if all parameters are None
        if (alternatives == None or info == None) and acceptedParameterDict == None:
            raise EmptyAcceptedParameterException("You must include either the alternatives and info parameters or the acceptedParameterDict parameter.")
        
        # alternatives and info parameters exist
        if alternatives != None and info != None:
            self._alternatives = alternatives
            
            # See if info is a dictionary
            try:
                self._info = info["text"]
                self._info_hyperlink_text = info["hyperlink_text"]
                self._info_hyperlink = info["hyperlink"]

                # See if info has formatting braces
                if self._info.find("{}") == -1:
                    raise MissingTextFormatException("You must provide a text formatting brace for the hyperlink to be inserted at.")

            except (KeyError, TypeError):
                self._info = info
                self._info_hyperlink_text = None
                self._info_hyperlink = None
        
        # acceptedParameterDict parameter exists
        elif acceptedParameterDict != None:
            self._alternatives = acceptedParameterDict["alternatives"]
            
            # See if info is a dictionary
            try:
                self._info = acceptedParameterDict["info"]["text"]
                self._info_hyperlink_text = acceptedParameterDict["info"]["hyperlink_text"]
                self._info_hyperlink = acceptedParameterDict["info"]["hyperlink"]

                # See if info has formatting braces
                if self._info.find("{}") == -1:
                    raise MissingTextFormatException("You must provide a text formatting brace for the hyperlink to be inserted at.")

            except (KeyError, TypeError):
                self._info = acceptedParameterDict["info"]
                self._info_hyperlink_text = None
                self._info_hyperlink = None
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def getAlternatives(self):
        """Returns the alternative names for this `AcceptedParameter` object.
        """

        return self._alternatives
    
    def getInfo(self, forHTML = False):
        """Returns the description of this `AcceptedParameter` object.
        """

        # See if hyperlinking exists
        if self._info_hyperlink != None:

            # See if hyperlinking is for HTML
            if forHTML:
                return self._info.format(
                    "<a href=\"{}\">{}</a>".format(
                        self._info_hyperlink,
                        self._info_hyperlink_text
                    )
                )
            else:
                return self._info.format(
                    "[{}]({})".format(
                        self._info_hyperlink_text,
                        self._info_hyperlink
                    )
                )

        return self._info

class Parameter:
    """Creates a new Parameter object
    There are two (2) different ways to make a `Parameter` object:
        1.) Clarify the info and optional parameters in the constructor.
        2.) Clarify a dictionary that holds the info and optional tag for the parameter.
    
    You must do one or the other.
    If they are both missing, an `EmptyParameterException` will occur.
    If both are included, the `info` and `optional` parameters will be used.

    If the `parameterDict` parameter is used, the following tags must be included:
        \"optional\"
        \"info\"
            Note: For the \"info\" tag, you can also give it a dictionary for dynamic hyperlinking. (Default is no hyperlink)
    The following tags are optional:
        \"accepted_parameters\" or \"accepted\" (Defaults to an empty dictionary)
    
    Parameters:
        info (str): The description of this parameter.
        optional (bool): Whether or not the parameter is optional.
        accepted_parameters | accepted (dict): A dictionary of `AcceptedParameter` objects.
    """

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Constructor
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def __init__(self, *, info = None, optional = None, accepted_parameters = None, accepted = None, parameterDict = None):
        """Creates a new Parameter object
        There are two (2) different ways to make a `Parameter` object:
            1.) Clarify the info and optional parameters in the constructor.
            2.) Clarify a dictionary that holds the info and optional tag for the parameter.
        
        You must do one or the other.
        If they are both missing, an `EmptyParameterException` will occur.
        If both are included, the `info` and `optional` parameters will be used.

        If the `parameterDict` parameter is used, the following tags must be included:
            \"optional\"
            \"info\"
                Note: For the \"info\" tag, you can also give it a dictionary for dynamic hyperlinking. (Default is no hyperlink)
        The following tags are optional:
            \"accepted_parameters\" or \"accepted\" (Defaults to an empty dictionary)
        
        Parameters:
            info (str): The description of this parameter.
            optional (bool): Whether or not the parameter is optional.
            accepted_parameters | accepted (dict): A dictionary of `AcceptedParameter` objects.
        """

        # Setup optional fields (defaults)
        self._accepted_parameters = {}

        # Check if all parameters are None
        if (info == None or optional == None) and parameterDict == None:
            raise EmptyParameterException("You must include either the info and optional parameters or the parameterDict parameter.")
        
        # info and optional parameters exist
        if info != None and optional != None:
            self._optional = optional

            # See if info is a dictionary
            try:
                self._info = info["text"]
                self._info_hyperlink_text = info["hyperlink_text"]
                self._info_hyperlink = info["hyperlink"]

                # See if info has formatting braces
                if self._info.find("{}") == -1:
                    raise MissingTextFormatException("You must provide a text formatting brace for the hyperlink to be inserted at.")

            except (KeyError, TypeError):
                self._info = info
                self._info_hyperlink_text = None
                self._info_hyperlink = None

            # the acceptedParameters list exists or...
            if accepted_parameters != None:
                self._accepted_parameters = accepted_parameters

            # ... the accepted list exists
            elif accepted != None:
                self._accepted_parameters = accepted
            
        
        # parameterDict parameter exists
        elif parameterDict != None:
            self._optional = parameterDict["optional"]

            # See if info is a dictionary
            try:
                self._info = parameterDict["info"]["text"]
                self._info_hyperlink_text = parameterDict["info"]["hyperlink_text"]
                self._info_hyperlink = parameterDict["info"]["hyperlink"]

                # See if info has formatting braces
                if self._info.find("{}") == -1:
                    raise MissingTextFormatException("You must provide a text formatting brace for the hyperlink to be inserted at.")

            except (KeyError, TypeError):
                self._info = parameterDict["info"]
                self._info_hyperlink_text = None
                self._info_hyperlink = None

            # the acceptedParameters tag exists or...
            if "accepted_parameters" in parameterDict:
                for parameter in parameterDict["accepted_parameters"]:
                    self._accepted_parameters[parameter] = AcceptedParameter(acceptedParameterDict = parameterDict["accepted_parameters"][parameter])
            
            # ...the accepted tag exists
            elif "accepted" in parameterDict:
                for parameter in parameterDict["accepted"]:
                    self._accepted_parameters[parameter] = AcceptedParameter(acceptedParameterDict = parameterDict["accepted"][parameter])
        
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def getInfo(self, forHTML = False):
        """Returns the description of this `Parameter` object.

        Returns:
            info (str)
        """

        # See if hyperlinking exists
        if self._info_hyperlink != None:

            # See if hyperlinking is for HTML
            if forHTML:
                return self._info.format(
                    "<a href=\"{}\">{}</a>".format(
                        self._info_hyperlink,
                        self._info_hyperlink_text
                    )
                )
            else:
                return self._info.format(
                    "[{}]({})".format(
                        self._info_hyperlink_text,
                        self._info_hyperlink
                    )
                )

        return self._info
    
    def isOptional(self):
        """Returns whether or not this `Parameter` object is optional.

        Returns:
            optional (bool)
        """

        return self._optional
    
    def getAcceptedParameters(self):
        """Returns the accepted parameters for this `Parameter` object.

        Returns:
            acceptedParameters (dict)
        """

        return self._accepted_parameters
    
    def getAcceptedParameter(self, acceptedParameter):
        """Returns an `AcceptedParameter` from this `Parameter` object.

        Returns:
            accepted_parameter (AcceptedParameter)
        
        Raises:
            NoSuchAcceptedParameterException - when the `accepted_parameter` parameter does not exist in this `Parameter` object.
        """

        if acceptedParameter in self._accepted_parameters:
            return self._accepted_parameters[acceptedParameter]
        
        raise NoSuchAcceptedParameterException("{} is not an accepted parameter.".format(acceptedParameter))

class Command:
    """Creates a new Command object.

    There are two (2) different ways to make a `Command` object:
        1.) Clarify the alternatives and info parameters in the constructor.
        2.) Clarify a dictionary that holds the alternatives and the info for the command.

    You must do one or the other.
    If they are both missing, an `EmptyCommandException` will occur.
    If both are included, the `alternatives` and `info` parameters will be used.

    If the `commandDict` parameter is used, the following tags must be included:
        \"alternatives\"
        \"info\"
            Note: For the \"info\" tag, you can also give it a dictionary for dynamic hyperlinking. (Default is no hyperlink)
    The following tags are optional:
        \"nsfw\" (Defaults to False)
        \"restriction_info\" (Defaults to an empty string)
        \"run_in_private\" (Defaults to True)
        \"can_be_deactivated\" (Defaults to True)
        \"server_moderator_only\" (Defaults to False)
        \"bot_moderator_only\" (Defaults to False)
        \"min_parameters\" (Defaults to amount of required parameters in parameters tag or 0 if None)
        \"max_parameters\" (Defaults to amount of parameter in parameters tag of 0 if None)
        \"parameters\" (Defaults to an empty dictionary)
        \"errors\" (Defaults to an empty dictionary)
        \"command\"
            Note: The \"command\" tag is just the name of the function to use. Your own function should be defined as a class variable.
                    This allows you to be able to have a for loop for the on_message event inside a cog.
                    When calling the command in the for loop, you just need to give it the parameters. The parameter logic should go in 
                    your function used for the command.
    """
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Constructor
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def __init__(self, *, 
        alternatives = None, info = None, 
        nsfw = None, restriction_info = None, 
        run_in_private = None, can_be_deactivated = None, 
        server_moderator_only = None, bot_moderator_only = None, 
        min_parameters = None, max_parameters = None, 
        parameters = None, errors = None, 
        command = None, commandDict = None):

        """Creates a new Command object.

        There are two (2) different ways to make a `Command` object:
            1.) Clarify the alternatives and info parameters in the constructor.
            2.) Clarify a dictionary that holds the alternatives and the info for the command.

        You must do one or the other.
        If they are both missing, an `EmptyCommandException` will occur.
        If both are included, the `alternatives` and `info` parameters will be used.

        If the `commandDict` parameter is used, the following tags must be included:
            \"alternatives\"
            \"info\"
                Note: For the \"info\" tag, you can also give it a dictionary for dynamic hyperlinking. (Default is no hyperlink)
        The following tags are optional:
            \"nsfw\" (Defaults to False)
            \"restriction_info\" (Defaults to an empty string)
            \"run_in_private\" (Defaults to True)
            \"can_be_deactivated\" (Defaults to True)
            \"server_moderator_only\" (Defaults to False)
            \"bot_moderator_only\" (Defaults to False)
            \"min_parameters\" (Defaults to amount of required parameters in parameters tag or 0 if None)
            \"max_parameters\" (Defaults to amount of parameter in parameters tag of 0 if None)
            \"parameters\" (Defaults to an empty dictionary)
            \"errors\" (Defaults to an empty dictionary)
            \"command\"
                Note: The \"command\" tag is just the name of the function to use. Your own function should be defined as a class variable.
                        This allows you to be able to have a for loop for the on_message event inside a cog.
                        When calling the command in the for loop, you just need to give it the parameters. The parameter logic should go in 
                        your function used for the command.
        """

        # Setup optional fields (defaults)
        self._nsfw = False
        self._restriction_info = ""
        self._restriction_info_hyperlink_text = None
        self._restriction_info_hyperlink = None
        self._run_in_private = True
        self._can_be_deactivated = True
        self._server_moderator_only = False
        self._bot_moderator_only = False
        self._min_parameters = None
        self._max_parameters = None
        self._parameters = {}
        self._errors = {}
        self._command = None

        # Check if all parameters are None
        if (alternatives == None or info == None) and commandDict == None:
            raise EmptyCommandException("You must include either the alternatives and info parameters or the commandDict parameter.")
        
        # alternatives and info parameters exist
        if alternatives != None and info != None:
            self._alternatives = alternatives

            # See if info is a dictionary
            try:
                self._info = info["text"]
                self._info_hyperlink_text = info["hyperlink_text"]
                self._info_hyperlink = info["hyperlink"]

                # See if info has formatting braces
                if self._info.find("{}") == -1:
                    raise MissingTextFormatException("You must provide a text formatting brace for the hyperlink to be inserted at.")

            except (KeyError, TypeError):
                self._info = info
                self._info_hyperlink_text = None
                self._info_hyperlink = None

            # the optional tags exist
            if nsfw != None:
                self._nsfw = nsfw
            if restriction_info != None:

                # See if restriction info is a dictionary
                try:
                    self._restriction_info = restriction_info["text"]
                    self._restriction_info_hyperlink_text = restriction_info["hyperlink_text"]
                    self._restriction_info_hyperlink = restriction_info["hyperlink"]

                    # See if info has formatting braces
                    if self._restriction_info.find("{}") == -1:
                        raise MissingTextFormatException("You must provide a text formatting brace for the hyperlink to be inserted at.")
                
                except (KeyError, TypeError):
                    self._restriction_info = restriction_info
                    self._restriction_info_hyperlink_text = None
                    self._restriction_info_hyperlink = None

            if run_in_private != None:
                self._run_in_private = run_in_private
            if can_be_deactivated != None:
                self._can_be_deactivated = can_be_deactivated
            if server_moderator_only != None:
                self._server_moderator_only = server_moderator_only
            if bot_moderator_only != None:
                self._bot_moderator_only = bot_moderator_only
            if min_parameters != None:
                self._min_parameters = min_parameters
            if max_parameters != None:
                self._max_parameters = max_parameters
            if parameters != None:

                # Iterate through parameters dictionary; Set min and max parameters if not already set
                minParameters = 0
                maxParameters = 0
                for parameter in parameters:

                    # Value is a dictionary, make it into a Parameter object
                    if type(parameters[parameter]) == dict:
                        parameters[parameter] = Parameter(parameterDict = parameters[parameter])
                    
                    if not parameters[parameter].isOptional():
                        minParameters += 1
                    
                    maxParameters += 1
                
                self._parameters = parameters
                
                if self._min_parameters == None:
                    self._min_parameters = minParameters
                if self._max_parameters == None:
                    self._max_parameters = maxParameters
            if errors != None:

                # Iterate through errors dictionary
                for error in errors:

                    # Value is a dictionary, make it into an Error object
                    if type(errors[error]) == dict:
                        errors[error] = Error(errorDict = errors[error])
                    
                self._errors = errors
            if command != None:
                self._command = None
        
        # commandDict parameter exists
        elif commandDict != None:
            self._alternatives = commandDict["alternatives"]

            # See if info is a dictionary
            try:
                self._info = commandDict["info"]["text"]
                self._info_hyperlink_text = commandDict["info"]["hyperlink_text"]
                self._info_hyperlink = commandDict["info"]["hyperlink"]

                # See if info has formatting braces
                if self._info.find("{}") == -1:
                    raise MissingTextFormatException("You must provide a text formatting brace for the hyperlink to be inserted at.")

            except (KeyError, TypeError):
                self._info = commandDict["info"]
                self._info_hyperlink_text = None
                self._info_hyperlink = None

            # the optional tags exist
            if "nsfw" in commandDict:
                self._nsfw = commandDict["nsfw"]
            if "restriction_info" in commandDict:

                # See if restriction info is a dictionary
                try:
                    self._restriction_info = commandDict["restriction_info"]["text"]
                    self._restriction_info_hyperlink_text = commandDict["restriction_info"]["hyperlink_text"]
                    self._restriction_info_hyperlink = commandDict["restriction_info"]["hyperlink"]

                    # See if info has formatting braces
                    if self._restriction_info.find("{}") == -1:
                        raise MissingTextFormatException("You must provide a text formatting brace for the hyperlink to be inserted at.")
                
                except (KeyError, TypeError):
                    self._restriction_info = commandDict["restriction_info"]
                    self._restriction_info_hyperlink_text = None
                    self._restriction_info_hyperlink = None

            if "run_in_private" in commandDict:
                self._run_in_private = commandDict["run_in_private"]
            if "can_be_deactivated" in commandDict:
                self._can_be_deactivated = commandDict["can_be_deactivated"]
            if "server_moderator_only" in commandDict:
                self._server_moderator_only = commandDict["server_moderator_only"]
            if "bot_moderator_only" in commandDict:
                self._bot_moderator_only = commandDict["bot_moderator_only"]
            if "min_parameters" in commandDict:
                self._min_parameters = commandDict["min_parameters"]
            if "max_parameters" in commandDict:
                self._max_parameters = commandDict["max_parameters"]
            if "parameters" in commandDict:

                # Iterate through parameters dictionary; Set min and max parameters if not already set
                minParameters = 0
                maxParameters = 0
                for parameter in commandDict["parameters"]:

                    # Value is a dictionary, make it into a Parameter object
                    if type(commandDict["parameters"][parameter]) == dict:
                        commandDict["parameters"][parameter] = Parameter(parameterDict = commandDict["parameters"][parameter])

                    if not commandDict["parameters"][parameter].isOptional():
                        minParameters += 1

                    maxParameters += 1
                
                self._parameters = commandDict["parameters"]
                
                if self._min_parameters == None:
                    self._min_parameters = minParameters
                if self._max_parameters == None:
                    self._max_parameters = maxParameters

            if "errors" in commandDict:

                # Iterate through errors dictionary
                for error in commandDict["errors"]:

                    # Value is a dictionary, make it into an Error object
                    if type(commandDict["errors"][error]) == dict:
                        commandDict["errors"][error] = Error(errorDict = commandDict["errors"][error])
                
                self._errors = commandDict["errors"]
            if "command" in commandDict:
                self._command = commandDict["command"]
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def getAlternatives(self):
        """Returns the alternatives for this `Command`.

        Returns:
            alternatives (list)
        """

        return self._alternatives
    
    def getInfo(self, forHTML = False, *, fancy = False):
        """Returns the description of this `Command` object.

        Returns:
            info (str)
        """

        # See if hyperlinking exists
        if self._info_hyperlink != None:

            # See if hyperlinking is for HTML
            if forHTML:

                # If the html is fancy, then get each part separately
                if fancy:
                    return {
                        "text": self._info.format(
                            self._info_hyperlink_text
                        ),
                        "link": self._info_hyperlink
                    }

                return self._info.format(
                    "<a href=\"{}\">{}</a>".format(
                        self._info_hyperlink,
                        self._info_hyperlink_text
                    )
                )
            else:
                return self._info.format(
                    "[{}]({})".format(
                        self._info_hyperlink_text,
                        self._info_hyperlink
                    )
                )

        return self._info
    
    def getRestrictionInfo(self, forHTML = False):
        """Returns any restriction info for this `Command` object.

        Returns:
            restrictionInfo (str)
        """

        # See if hyperlinking exists
        if self._restriction_info_hyperlink != None:

            # See if hyperlinking is for HTML
            if forHTML:
                return self._restriction_info.format(
                    "<a href=\"{}\">{}</a>".format(
                        self._restriction_info_hyperlink,
                        self._restriction_info_hyperlink_text
                    )
                )
            else:
                return self._restriction_info.format(
                    "[{}]({})".format(
                        self._restriction_info_hyperlink_text,
                        self._restriction_info_hyperlink
                    )
                )
        
        return self._restriction_info
    
    def isNSFW(self):
        """Returns whether or not the command should only be run in NSFW channels.

        Returns:
            nsfw (bool)
        """

        return self._nsfw
    
    def canBeRunInPrivate(self):
        """Returns whether or not this `Command` object can be run in a DMChannel or a GroupChannel.

        Returns:
            runInPrivate (bool)
        """

        return self._run_in_private
    
    def canBeDeactivated(self):
        """Returns whether or not this `Command` object can be deactivated.

        Returns:
            canBeDeactivated (bool)
        """

        return self._can_be_deactivated
    
    def isServerModeratorCommand(self):
        """Returns whether or not this `Command` object can only be run by a server moderator.

        Returns:
            serverModeratorCommand (bool)
        """

        return self._server_moderator_only
    
    def isBotModeratorCommand(self):
        """Returns whether or not this `Command` object can only be run by a bot moderator.

        Returns:
            botModeratorCommand (bool)
        """

        return self._bot_moderator_only
    
    def getMinParameters(self):
        """Returns the minimum amount of parameters this `Command` object takes.

        Returns:
            minParameters (int)
        """

        if self._min_parameters == None:
            return 0
        return self._min_parameters
    
    def getMaxParameters(self):
        """Returns the maximum amount of parameters this `Command` object takes.

        Returns:
            maxParameters (int)
        """

        if self._max_parameters == None:
            return 0
        return self._max_parameters
    
    def getParameters(self):
        """Returns the parameters for this `Command` object.

        Returns:
            parameters (dict)
        """

        return self._parameters
    
    def getParameter(self, parameter):
        """Returns a `Parameter` from this `Command` object.

        Parameters:
            parameter (str): The identifier of the `Parameter`

        Returns:
            parameters (dict)

        Raises:
            NoSuchParameterException: when the `parameter` does not exist
        """

        if parameter in self._parameters:
            return self._parameters[parameter]
        
        raise NoSuchParameterException("{} is not a parameter.".format(parameter))
    
    def getAcceptedParameters(self, parameter):
        """Returns the accepted parameters for a `Parameter` object.

        Parameters:
            parameter (str): The identifier of the `Parameter`

        Returns:
            acceptedParameters (dict)
        
        Raises:
            NoSuchParameterException: when the `parameter` does not exist
        """

        if parameter in self._parameters:
            return self._parameters[parameter].getAcceptedParameters()
        
        raise NoSuchParameterException("{} is not a parameter.".format(parameter))
    
    def getAcceptedParameter(self, parameter, acceptedParameter):
        """Returns an `AcceptedParameter` from this `Parameter` object.

        Parameters:
            parameter (str): The identifier of the `Parameter`
            acceptedParameter (str): The identifier of the `AcceptedParameter`

        Returns:
            acceptedParameter (AcceptedParameter)
        
        Raises:
            NoSuchParameterException: when the `parameter` does not exist
            NoSuchAcceptedParameterException: when the `acceptedParameter` does not exist
        """

        if parameter in self._parameters:
            return self._parameters[parameter].getAcceptedParameter(acceptedParameter)
        
        raise NoSuchParameterException("{} is not a parameter.".format(parameter))
    
    def getErrors(self):
        """Returns the `Error`s in this `Command` object.

        Returns:
            errors (list)
        """
        
        return self._errors
    
    def getError(self, errorType):
        """Returns an `Error` from this `Command` object.

        Parameters:
            errorType (str): The identifier of the `Error`
        
        Returns:
            error (Error)
        
        Raises:
            NoSuchErrorException: when the `errorType` does not exist
        """
        
        if errorType in self._errors:
            return self._errors[errorType]
        
        raise NoSuchErrorException("{} is not an error.".format(errorType))
    
    def getCommand(self):
        """Returns the function used to run the command

        Returns:
            command (func)
        """
        
        return self._command
    
    def getErrorMessage(self, errorType):
        """Returns a random error message from this `Command` object.

        Parameters:
            errorType (str): The identifier of the `Error`
        
        Returns:
            errorMessage (str)
        
        Raises:
            NoSuchErrorException: when the `errorType` does not exist
        """
        
        if errorType in self._errors:
            return self._errors[errorType].getMessage()
        
        raise NoSuchErrorException("{} is not an error.".format(errorType))

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Setters
    # # # # # # # # # # # # # # # # # # # # # # # # # 

    def setRunInPrivate(self, run_in_private):
        """Sets whether or not the Command can be run in a Private Message.

        Parameters:
            run_in_private (bool): Whether or not the Command can be run in a Private Message.
        """

        self._run_in_private = run_in_private
        if run_in_private == None:
            self._run_in_private = False

    def setNSFW(self, nsfw):
        """Sets whether or not the Command is an NSFW command.

        Parameters:
            nsfw (bool): Whether or not the Command is NSFW.
        """

        self._nsfw = nsfw
        if nsfw == None:
            self._nsfw = False
    
    def setServerModeratorOnly(self, server_moderator_only):
        """Sets whether or not the Command can only
        be run by Server Moderators.

        Parameters:
            server_moderator_only (bool): Whether or not the Command can only be run by Server Moderators.
        """
        
        self._server_moderator_only = server_moderator_only
        if server_moderator_only == None:
            self._server_moderator_only = False
    
    def setBotModeratorOnly(self, bot_moderator_only):
        """Sets whether or not the Command can only
        be run by Bot Moderators.

        Parameters:
            bot_moderator_only (bool): Whether or not the Command can only be run by Bot Moderators.
        """
        
        self._bot_moderator_only = bot_moderator_only
        if bot_moderator_only == None:
            self._bot_moderator_only = False

    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Help Menu, HTML, and Markdown
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    
    def getHelp(self, *, inDepth = False, isNSFW = False, maxFieldLength = 1000):
        """Returns a dictionary giving help on this `Command` object.

        A short help dictionary (not inDepth) will include the following:
            1.) The primary command name.
            2.) Optional and required parameters surrounded by [] and <> respectively.
            3.) Info on what the command does
        
        A long help dictionary (inDepth) will include the following:
            1.) Alternative names for the command.
            2.) Optional and required parameters surrounded by [] and <> respectively.
            3.) Info on what the command does
            4.) Info on what each parameter is for
            5.) Info on any accepted parameters and what they represent
        
        The help dictionary will have the following tags:
            \"title\": The primary help information. 
            \"restriction\": The restriction info. (An empty string if it is not inDepth)
            \"accepted\": The accepted parameter information. (An empty dictionary if it is not inDepth)
        
        Parameters:
            inDepth (bool): Whether or not to get in-depth help for a command. (Defaults to False)
            isNSFW (bool): Whether or not to censor any NSFW material. (Defaults to False)
            maxFieldLength (int): The maximum length of a single field if inDepth. (Defaults to 1000)
        
        Returns:
            help (dict)
        """

        # Set default values
        dictRestriction = ""
        dictAccepted = {}

        # Setup Placeholder Parameters Text (Shows on both inDepth and not inDepth)
        placeholderParameters = []
        for parameter in self.getParameters():
            placeholderParameters.append("{}{}{}".format(
                "[" if self.getParameters()[parameter].isOptional() else "<",
                parameter,
                "]" if self.getParameters()[parameter].isOptional() else ">"
            ))
        placeholders = " ".join(placeholderParameters)

        # See if inDepth
        if inDepth:

            # Setup Accepted Parameter Fields
            acceptedParameters = {}
            for parameter in self.getParameters():
                parameterName = parameter
                parameterObject = self.getParameters()[parameter]

                # Only add if there are accepted parameters
                if len(parameterObject.getAcceptedParameters()) > 0:
                    acceptedParameters[parameterName] = ""

                    # Iterate through all accepted parameters and add them to a single string
                    for acceptedParameter in parameterObject.getAcceptedParameters():
                        acceptedObject = parameterObject.getAcceptedParameters()[acceptedParameter]

                        # Add parameter info to string
                        acceptedParameters[parameterName] += "`{}` - {}\n".format(
                            " | ".join(acceptedObject.getAlternatives()),
                            acceptedObject.getInfo()
                        )
            
            # Add Accepted Parameter Fields
            for parameter in acceptedParameters:

                # Setup fields
                fields = []
                fieldText = ""
                acceptedParams = acceptedParameters[parameter].split("\n")

                # Keep each parameter underneath the maxFieldLength
                for param in acceptedParams:

                    accepted = censor(param) if not isNSFW else param
                    accepted += "\n"

                    if len(fieldText) + len(accepted) >= maxFieldLength:
                        fields.append(fieldText)
                        fieldText = ""
                    
                    fieldText += accepted
                
                if len(fieldText) > 0:
                    fields.append(fieldText)
                
                # Add fields to accepted dict
                dictAccepted[parameter] = fields
            
            # Set title and fields
            dictTitle = "`{} {}` - {}{}{}{}\n".format(
                censor(" | ".join(self.getAlternatives()), True) if not isNSFW else " | ".join(self.getAlternatives()),
                censor(placeholders) if not isNSFW else placeholders,
                "**`NSFW`** " if self.isNSFW() else "",
                "**`Server Mod`** " if self.isServerModeratorCommand() else "",
                "**`Bot Mod`** " if self.isBotModeratorCommand() else "",
                censor(self.getInfo()) if not isNSFW else self.getInfo()
            )
            dictRestriction = self.getRestrictionInfo()
        
        # Not inDepth
        else:

            dictTitle = "`{} {}` - {}{}{}{}\n".format(
                censor(self.getAlternatives()[0], True) if not isNSFW else self.getAlternatives()[0],
                censor(placeholders) if not isNSFW else placeholders,
                "**``NSFW``** " if self.isNSFW() else "",
                "**`Server Mod`** " if self.isServerModeratorCommand() else "",
                "**`Bot Mod`** " if self.isBotModeratorCommand() else "",
                censor(self.getInfo()) if not isNSFW else self.getInfo()
            )
        
        # Return the help dictionary
        return {
            "title": dictTitle,
            "restriction": dictRestriction,
            "accepted": dictAccepted
        }
    
    def getHTMLNew(self):
        """Returns the HTML rendering text for the `Command`.

        Returns:
            htmlText (str)
        """

        # Setup HTML Text
        html = ""

        # Add Commands and Placeholder Parameters
        placeholderParameters = []
        for parameter in self.getParameters():
            placeholderParameters.append("{}{}{}".format(
                "[" if self.getParameters()[parameter].isOptional() else "&lt;",
                parameter,
                "]" if self.getParameters()[parameter].isOptional() else "&gt;"
            ))
        
        html += ("  <li><code>{} {}</code> - <strong><code>{}</code></strong><strong><code>{}</code></strong><strong><code>{}</code></strong>{}</li>\n".format(
            " | ".join(self.getAlternatives()),
            " ".join(placeholderParameters) if len(placeholderParameters) > 0 else "",
            "NSFW " if self.isNSFW() else "",
            "Server Mod " if self.isServerModeratorCommand() else "",
            "Bot Mod " if self.isBotModeratorCommand() else "",
            self.getInfo(True)
        ))

        # Setup Accepted Parameters
        html += "  <ul>\n"
        for parameter in self.getParameters():
            parameterName = parameter
            parameterObject = self.getParameters()[parameter]

            # Only add if there are accepted parameters
            if len(parameterObject.getAcceptedParameters()) > 0:
                html += ("  <li>{}</li>\n".format(
                    "Accepted Parameters for <code>{}</code>\n".format(
                        parameterName
                    )
                ))

                # Iterate through all accepted parameters and add them
                html += "    <ul>\n"
                for acceptedParameter in parameterObject.getAcceptedParameters():
                    acceptedObject = parameterObject.getAcceptedParameters()[acceptedParameter]

                    html += ("      <li><code>{}</code> - {}</li>\n".format(
                        " | ".join(acceptedObject.getAlternatives()),
                        acceptedObject.getInfo(True)
                    ))
                html += "    </ul>\n"
        html += "  </ul>\n"

        return html

    def getHTML(self):
        """Returns the HTML rendering text for the `Command`.

        Returns:
            htmlText (str)
        """

        # Setup HTML text
        html = ""

        # Add Commands and Placeholder Parameters
        placeholderParameters = []
        for parameter in self.getParameters():
            placeholderParameters.append("{}{}{}".format(
                "[" if self.getParameters()[parameter].isOptional() else "&lt;",
                parameter,
                "]" if self.getParameters()[parameter].isOptional() else "&gt;"
            ))
        
        html += (
            "        <span class=\"command\">{} {}</span> -\n" +
            "        <span class=\"commandTags\">{}</span>{}\n" +
            "        <span class=\"commandTags\">{}</span>{}\n" +
            "        <span class=\"commandTags\">{}</span>{}\n" +
            "        <span class=\"commandInfo\">{}</span>\n"
        ).format(
            " | ".join(self.getAlternatives()),
            " ".join(placeholderParameters) if len(placeholderParameters) > 0 else "",
            "NSFW" if self.isNSFW() else "", ";" if self.isNSFW() else "",
            "Server Mod" if self.isServerModeratorCommand() else "", ";" if self.isServerModeratorCommand() else "",
            "Bot Mod" if self.isBotModeratorCommand() else "", ";" if self.isBotModeratorCommand() else "",
            self.getInfo(True) if self._info_hyperlink == None else self.getInfo(True, fancy = True)["text"]
        )

        # Setup Accepted Parameters
        html += "        <ul>\n"
        for parameter in self.getParameters():
            parameterName = parameter
            parameterObject = self.getParameters()[parameter]

            # Only add if there are accepted parameters
            if len(parameterObject.getAcceptedParameters()) > 0:
                html += ("          <li class=\"commandInfo\">{}</li>\n".format(
                    "Accepted Parameters for <code class=\"command\">{}</code>".format(
                        parameterName
                    )
                ))

                # Iterate through all accepted parameters and add them
                html += "          <ul>\n"
                for acceptedParameter in parameterObject.getAcceptedParameters():
                    acceptedObject = parameterObject.getAcceptedParameters()[acceptedParameter]

                    html += ("            <li class=\"commandInfo\"><code class=\"command\">{}</code> - {}</li>\n".format(
                        " | ".join(acceptedObject.getAlternatives()),
                        acceptedObject.getInfo(True)
                    ))
                html += "          </ul>\n"
        html += "        </ul>\n"

        return (
            "      <a {}>\n" + 
            html +
            "      </a>\n"
        ).format(
            "" if self._info_hyperlink == None else "href=\"{}\"".format(
                self.getInfo(True, fancy = True)["link"]
            )
        )
    
    def getMarkdown(self):
        """Returns the Markdown render text for the `Command`.\n

        Returns:
            markdownText (str)
        """

        # Setup Markdown Text
        markdown = ""

        # Add Commands and Placeholder Parameters
        placeholderParameters = []
        for parameter in self.getParameters():
            placeholderParameters.append("{}{}{}".format(
                "[" if self.getParameters()[parameter].isOptional() else "<",
                parameter,
                "]" if self.getParameters()[parameter].isOptional() else ">"
            ))
        
        markdown += ("  * `{} {}` - {}{}{}{}\n".format(
            " | ".join(self.getAlternatives()),
            " ".join(placeholderParameters) if len(placeholderParameters) > 0 else "",
            "**`NSFW`** " if self.isNSFW() else "",
            "**`Server Mod`** " if self.isServerModeratorCommand() else "",
            "**`Bot Mod`** " if self.isBotModeratorCommand() else "",
            self.getInfo()
        ))

        # Setup Accepted Parameters
        for parameter in self.getParameters():
            parameterName = parameter
            parameterObject = self.getParameters()[parameter]

            # Only add if there are accepted parameters
            if len(parameterObject.getAcceptedParameters()) > 0:
                markdown += ("    * {}\n".format(
                    "Accepted Parameters for `{}`".format(
                        parameterName
                    )
                ))

                # Iterate through all accepted parameters and add them
                for acceptedParameter in parameterObject.getAcceptedParameters():
                    acceptedObject = parameterObject.getAcceptedParameters()[acceptedParameter]

                    markdown += ("      * `{}` - {}\n".format(
                        " | ".join(acceptedObject.getAlternatives()),
                        acceptedObject.getInfo()
                    ))
        
        return markdown