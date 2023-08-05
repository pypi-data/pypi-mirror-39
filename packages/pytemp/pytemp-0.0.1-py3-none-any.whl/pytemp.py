import sys


"""
This is a python module to convert temperatures from one unit to another
"""
def pytemp(temp, initial, expected):
    """
        :param temp: An integer value of the temperature to be converted
        :param inital: A string describing the current unit the temperature is in
        :param expected: A string describing the expected unit the temperature should be converted to
        :return: a float representing the new temperature after conversion


        convert from 40 degree kelvin to fahrenheit and back

        >>> pytemp(40,'kelvin', 'fahrenheit')
        -387.66999999999996
        >>> pytemp(40,'k', 'f')
        -387.66999999999996
        >>> pytemp(-387.66999999999996,'fahrenheit','kelvin')
        40.0
        >>> pytemp(-387.66999999999996,'f','k')
        40.0

        convert from 40 degree celsius to fahrenheit and back

        >>> pytemp(40,'celsius', 'fahrenheit')
        104.0
        >>> pytemp(40,'c', 'f')
        104.0
        >>> pytemp(104.0,'fahrenheit','celsius')
        40.0
        >>> pytemp(104.0,'f','c')
        40.0

        convert from 40 degree kelvin to celsius and back

        >>> pytemp(40,'kelvin', 'celsius')
        -233.14999999999998
        >>> pytemp(40,'k', 'c')
        -233.14999999999998
        >>> pytemp(-233.14999999999998,'celsius','kelvin')
        40.0
        >>> pytemp(-233.14999999999998,'c','k')
        40.0
    """
    units = ["fahrenheit", "f", "celsius", "c", "kelvin", "k"]


    """
        This line throw error and exit the program for invalid input type
    """
    if initial.lower() not in units:
        sys.exit("initial temperature unit must be one of the fahrenheit, f, celsius, c, kelvin or k")
    elif expected.lower() not in units:
        sys.exit("expected temperature unit must be one of the fahrenheit, f, celsius, c, kelvin or k")
    try:
        """
        This detects initial and expected and returns the desired conversion
        """
        if (initial.lower() == "fahrenheit" or initial.lower() == "f") \
            and (expected.lower() == "celsius" or expected.lower() == "c"):
            return (temp-32)/1.8

        elif (initial.lower() == "celsius" or initial.lower() == "c")  \
            and (expected.lower() == "fahrenheit" or expected.lower() == "f"):
            return temp*1.8 + 32
        

        elif (initial.lower() == "kelvin" or initial.lower() == "k")  \
            and (expected.lower() == "fahrenheit" or expected.lower() == "f"):
            return (temp-273.15) * 9/5 + 32
        
        elif (initial.lower() == "fahrenheit" or initial.lower() == "f")  \
            and (expected.lower() == "kelvin" or expected.lower() == "k"):
            return (temp-32) * 5/9 + 273.15
        
        elif (initial.lower() == "celsius" or initial.lower() == "c")  \
            and (expected.lower() == "kelvin" or expected.lower() == "k"):
            return temp + 273.15

        elif (initial.lower() == "kelvin" or initial.lower() == "k")  \
            and (expected.lower() == "celsius" or expected.lower() == "c"):
            return temp-273.15
        else:
            sys.exit("cannot convert {} from {} to {}".format(temp,initial, expected))          
    except Exception:
        sys.exit("cannot convert {} from {} to {}".format(temp,initial, expected))




if __name__ == "__main__":
    import doctest
    doctest.testmod()