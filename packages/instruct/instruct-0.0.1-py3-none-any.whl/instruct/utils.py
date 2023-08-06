import typing


def parse_typedef_to_test(typedefs):
    """Convert type definitions to a set of codegen tests

    This is a safety and is probably expensive (compared to no safeties).

    This is meant for use in development/staging builds (aggressively check EVERYTHING) and
    in production when untrusted input is expected.

    Simple things like:
        str -> isinstance(val, str)
        (str, int) -> isinstance(val, (str, int))
    are easy to catch.

    Complex cases:
        List[Union[str, Tuple[int, str], List[int]]] ->

        def var_isinstance(val):
            if not isinstance(val, list):
                return False
            for item in val:
                if not isinstance(item, (str, tuple, list)):
                    return False
                # for every non-typing item, continue if we match the type
                if isinstance(item, str):
                    continue
                # every complex item is broken down into if true->continue
                if var_1_isinstance(item):
                    continue
                if var_2_isinstance(item):
                    continue
                return False
            return True
        def var_1_isintance(val):
            if not isinstance(val, (int, str)):
                return False
            return True

    In cases where we have something like:
        Let C(Base) denote a class derived from Base and D(Base) denote a different
        class:

        Union[C, D] will mean that we can't process nested JSON/dictionaries
        without either knowing which class to pick first. Randomly applying the constructor
        is a bad idea.

        Cases:
            - C/D can be chosen based solely on ``value``
            - C/D can be chosen based on the state of the object after construction
            - C/D can be chosen in the parent state before construction is complete but after
                other variables

        This means that we have some requirement for:
            "When constraints are satisfied, then apply class to value"
        where ``constraints`` may be:


    """
    if not isinstance(typedefs, tuple):
        typedefs = (typedefs,)

    if all(getattr(typecls, 'module', None) != 'typing' and
            not isinstance(typecls, (typing.TypeVar, typing.TypingMeta, typing.Type))
            for typecls in typedefs):
        # all non-typing classes
        return '''
        def {varname}_isinstance(val):
            if not isinstance(val, {varname}_types):
                return False
            return True
        '''
    # Okay, we have some typing items!
    ...
